#!/usr/bin/env python3
"""
Template Sanitization Script
Removes vendor-specific branding and localizes assets from HTML templates
"""

import os
import re
import shutil
import urllib.request
from pathlib import Path
from typing import List, Dict, Set
from urllib.parse import urlparse
import argparse

try:
    from bs4 import BeautifulSoup
    import yaml
except ImportError:
    print("Missing dependencies. Please install:")
    print("  pip install beautifulsoup4 pyyaml")
    exit(1)


class TemplateSanitizer:
    def __init__(self, config_path: str = "sanitize-config.yml"):
        """Initialize the sanitizer with configuration"""
        self.config = self._load_config(config_path)
        self.report = []
        self.processed_files = 0
        self.downloaded_assets = set()

    def _load_config(self, config_path: str) -> Dict:
        """Load YAML configuration file"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    def find_html_files(self, root_dir: str = ".") -> List[Path]:
        """Find all HTML files matching patterns"""
        html_files = []
        root = Path(root_dir)

        for pattern in self.config['files']['patterns']:
            for file_path in root.glob(pattern):
                # Check if file should be excluded
                should_exclude = False
                for exclude_pattern in self.config['files']['exclude']:
                    if file_path.match(exclude_pattern):
                        should_exclude = True
                        break

                if not should_exclude and file_path.is_file():
                    html_files.append(file_path)

        return html_files

    def backup_file(self, file_path: Path):
        """Create a backup of the file"""
        if self.config['output']['backup']:
            backup_path = str(file_path) + self.config['output']['backup_suffix']
            shutil.copy2(file_path, backup_path)
            self.log(f"Created backup: {backup_path}")

    def download_asset(self, url: str, local_path: Path) -> bool:
        """Download an external asset to local path"""
        try:
            # Create directory if it doesn't exist
            local_path.parent.mkdir(parents=True, exist_ok=True)

            # Download the file
            urllib.request.urlretrieve(url, local_path)
            self.downloaded_assets.add(str(local_path))
            self.log(f"Downloaded: {url} -> {local_path}")
            return True
        except Exception as e:
            self.log(f"Failed to download {url}: {e}", level="ERROR")
            return False

    def get_relative_path(self, from_file: Path, to_file: Path) -> str:
        """Get relative path from one file to another"""
        try:
            return os.path.relpath(to_file, from_file.parent)
        except ValueError:
            # If on different drives (Windows), return absolute path
            return str(to_file)

    def should_download_asset(self, url: str) -> bool:
        """Check if asset URL should be downloaded"""
        if not self.config['assets']['download_external']:
            return False

        parsed = urlparse(url)
        for domain in self.config['assets']['vendor_domains']:
            if domain in parsed.netloc:
                return True
        return False

    def sanitize_metadata(self, soup: BeautifulSoup, file_path: Path) -> int:
        """Remove and update metadata tags"""
        changes = 0

        # Remove vendor-specific elements
        for element_config in self.config['remove_elements']:
            selector = element_config['selector']
            contains = element_config.get('contains')

            elements = soup.select(selector)
            for element in elements:
                if contains:
                    # Check if element contains the pattern
                    text = element.get_text() if element.string is None else str(element.string)
                    attrs = ' '.join([str(v) for v in element.attrs.values()])
                    combined = text + ' ' + attrs

                    if re.search(contains, combined, re.IGNORECASE):
                        element.decompose()
                        changes += 1
                        self.log(f"Removed {selector} containing '{contains}'")
                else:
                    element.decompose()
                    changes += 1
                    self.log(f"Removed {selector}")

        # Update title
        title_tag = soup.find('title')
        if title_tag:
            new_title = self._get_page_title(file_path)
            old_title = title_tag.string
            title_tag.string = new_title
            changes += 1
            self.log(f"Updated title: {old_title} -> {new_title}")

        # Update description
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag:
            new_desc = self._get_page_description(file_path)
            old_desc = desc_tag.get('content', '')
            desc_tag['content'] = new_desc
            changes += 1
            self.log(f"Updated description")

        # Update OG tags
        og_title = soup.find('meta', property='og:title')
        if og_title:
            og_title['content'] = self._get_page_title(file_path)
            changes += 1

        og_desc = soup.find('meta', property='og:description')
        if og_desc:
            og_desc['content'] = self._get_page_description(file_path)
            changes += 1

        # Update Twitter tags
        twitter_title = soup.find('meta', attrs={'name': 'twitter:title'})
        if twitter_title:
            twitter_title['content'] = self._get_page_title(file_path)
            changes += 1

        twitter_desc = soup.find('meta', attrs={'name': 'twitter:description'})
        if twitter_desc:
            twitter_desc['content'] = self._get_page_description(file_path)
            changes += 1

        return changes

    def _get_page_title(self, file_path: Path) -> str:
        """Generate appropriate title for a page"""
        personal = self.config['personal']

        # Check if it's a special page
        if 'contact' in str(file_path).lower():
            return self.config['pages']['contact']['title']

        # Check if it's a case study
        if 'work/' in str(file_path):
            project_name = file_path.parent.name.replace('-', ' ').title()
            template = self.config['pages']['case_studies']['title_template']
            return template.format(project_name=project_name)

        # Default homepage title
        return f"{personal['name']} - {personal['title']}"

    def _get_page_description(self, file_path: Path) -> str:
        """Generate appropriate description for a page"""
        personal = self.config['personal']

        # Check if it's a special page
        if 'contact' in str(file_path).lower():
            return self.config['pages']['contact']['description']

        # Check if it's a case study
        if 'work/' in str(file_path):
            project_name = file_path.parent.name.replace('-', ' ').title()
            template = self.config['pages']['case_studies']['description_template']
            return template.format(project_name=project_name)

        # Default description
        return personal['description']

    def sanitize_assets(self, soup: BeautifulSoup, file_path: Path) -> int:
        """Download and localize external assets"""
        changes = 0
        assets_dir = Path(self.config['assets']['local_path'])

        # Process favicons
        for link in soup.find_all('link', rel='icon'):
            href = link.get('href', '')
            if self.should_download_asset(href):
                # Determine filename
                if 'light' in href or 'prefers-color-scheme: light' in str(link):
                    filename = 'favicon-light.png'
                elif 'dark' in href or 'prefers-color-scheme: dark' in str(link):
                    filename = 'favicon-dark.png'
                else:
                    filename = 'favicon.png'

                local_path = assets_dir / filename
                if self.download_asset(href, local_path):
                    # Update href to relative path
                    link['href'] = self.get_relative_path(file_path, local_path)
                    changes += 1

        # Process OG images
        og_image = soup.find('meta', property='og:image')
        if og_image and self.should_download_asset(og_image.get('content', '')):
            local_path = assets_dir / 'og-preview.png'
            if self.download_asset(og_image['content'], local_path):
                og_image['content'] = self.get_relative_path(file_path, local_path)
                changes += 1

        # Process Twitter images
        twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
        if twitter_image and self.should_download_asset(twitter_image.get('content', '')):
            local_path = assets_dir / 'og-preview.png'
            if self.download_asset(twitter_image['content'], local_path):
                twitter_image['content'] = self.get_relative_path(file_path, local_path)
                changes += 1

        return changes

    def sanitize_attributes(self, soup: BeautifulSoup) -> int:
        """Replace vendor-specific attributes"""
        changes = 0

        for replacement in self.config['attribute_replacements']:
            from_attr = replacement['from']
            to_attr = replacement['to']

            # Find all elements with the attribute
            for element in soup.find_all(attrs={from_attr: True}):
                element[to_attr] = element[from_attr]
                del element[from_attr]
                changes += 1
                self.log(f"Replaced attribute: {from_attr} -> {to_attr}")

        return changes

    def sanitize_css(self, content: str) -> tuple[str, int]:
        """Remove vendor-specific CSS patterns"""
        import re
        changes = 0
        original_content = content

        # Remove Framer badge container CSS
        # Matches: @supports...{#__framer-badge-container{...}}#__framer-badge-container{...}
        pattern = r'@supports\s*\(z-index:calc\(infinity\)\)\s*\{#__framer-badge-container\{[^}]+\}\}#__framer-badge-container\{[^}]+\}'
        content = re.sub(pattern, '', content)

        if content != original_content:
            changes += 1
            self.log("Removed Framer badge container CSS")

        return content, changes

    def process_file(self, file_path: Path):
        """Process a single HTML file"""
        self.log(f"\n{'='*60}")
        self.log(f"Processing: {file_path}")
        self.log(f"{'='*60}")

        # Backup original file
        self.backup_file(file_path)

        # Read and parse HTML
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # First pass: sanitize CSS patterns in raw HTML
        content, css_changes = self.sanitize_css(content)

        soup = BeautifulSoup(content, 'html.parser')

        # Track changes
        total_changes = css_changes

        # Sanitize metadata
        total_changes += self.sanitize_metadata(soup, file_path)

        # Sanitize assets
        total_changes += self.sanitize_assets(soup, file_path)

        # Sanitize attributes
        total_changes += self.sanitize_attributes(soup)

        # Write back to file if changes were made
        if total_changes > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(soup))

            self.log(f"✓ Made {total_changes} changes to {file_path}")
            self.processed_files += 1
        else:
            self.log(f"✓ No changes needed for {file_path}")

    def log(self, message: str, level: str = "INFO"):
        """Log a message to the report"""
        log_entry = f"[{level}] {message}"
        self.report.append(log_entry)

        if self.config['output']['verbose']:
            print(log_entry)

    def generate_report(self):
        """Generate final report"""
        summary = f"""
{'='*60}
SANITIZATION COMPLETE
{'='*60}

Files Processed: {self.processed_files}
Assets Downloaded: {len(self.downloaded_assets)}

Downloaded Assets:
"""
        for asset in sorted(self.downloaded_assets):
            summary += f"  - {asset}\n"

        summary += f"\nFull log:\n{'-'*60}\n"
        summary += '\n'.join(self.report)

        # Print to console
        print(summary)

        # Save to file if configured
        if self.config['output']['report']:
            report_file = self.config['output']['report_file']
            with open(report_file, 'w') as f:
                f.write(summary)
            print(f"\nReport saved to: {report_file}")

    def run(self, root_dir: str = "."):
        """Run the sanitization process"""
        self.log("Starting template sanitization...")

        # Find all HTML files
        html_files = self.find_html_files(root_dir)
        self.log(f"Found {len(html_files)} HTML files to process")

        # Process each file
        for file_path in html_files:
            try:
                self.process_file(file_path)
            except Exception as e:
                self.log(f"Error processing {file_path}: {e}", level="ERROR")

        # Generate final report
        self.generate_report()


def main():
    parser = argparse.ArgumentParser(
        description="Sanitize HTML templates by removing vendor branding"
    )
    parser.add_argument(
        '--config',
        default='sanitize-config.yml',
        help='Path to configuration file (default: sanitize-config.yml)'
    )
    parser.add_argument(
        '--dir',
        default='.',
        help='Root directory to process (default: current directory)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )

    args = parser.parse_args()

    # Check if config exists
    if not os.path.exists(args.config):
        print(f"Error: Config file not found: {args.config}")
        print("Create one using 'sanitize-config.yml' as a template")
        return 1

    # Run sanitizer
    sanitizer = TemplateSanitizer(args.config)
    sanitizer.run(args.dir)

    return 0


if __name__ == '__main__':
    exit(main())
