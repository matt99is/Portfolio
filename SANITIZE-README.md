# Template Sanitization Script

Automatically remove vendor branding (Framer, Resize, etc.) from HTML templates and localize external assets.

## Features

- ✅ Removes vendor-specific scripts and meta tags
- ✅ Updates page titles and descriptions
- ✅ Downloads and localizes external assets (favicons, OG images)
- ✅ Updates asset references to local paths
- ✅ Replaces vendor-specific HTML attributes
- ✅ Creates backups before modifying files
- ✅ Generates detailed reports
- ✅ Configurable via YAML file

## Installation

### Prerequisites

Python 3.6+ required. Install dependencies:

```bash
pip install beautifulsoup4 pyyaml
```

Or using pip3:

```bash
pip3 install beautifulsoup4 pyyaml
```

## Quick Start

### 1. Configure Your Details

Edit `sanitize-config.yml` with your personal information:

```yaml
personal:
  name: "Your Name"
  title: "Your Title"
  description: "Your description..."
```

### 2. Run the Script

```bash
python3 sanitize-template.py
```

That's it! The script will:
- Find all HTML files
- Remove vendor branding
- Download and localize assets
- Update all references
- Create backups
- Generate a report

## Usage

### Basic Usage

Process current directory:
```bash
python3 sanitize-template.py
```

### Advanced Options

Process specific directory:
```bash
python3 sanitize-template.py --dir /path/to/template
```

Use custom config file:
```bash
python3 sanitize-template.py --config my-config.yml
```

Preview changes without modifying files:
```bash
python3 sanitize-template.py --dry-run
```

## Configuration

### Personal Information

```yaml
personal:
  name: "Matt"
  title: "UX Designer specialising in e-commerce"
  description: "Your main description..."
```

### Page-Specific Overrides

```yaml
pages:
  contact:
    title: "Contact - Your Name"
    description: "Contact page description..."
```

### Remove Patterns

Specify keywords to search for and remove:

```yaml
remove_patterns:
  - "framer"
  - "resize"
  - "template"
```

### Asset Handling

Configure how external assets are handled:

```yaml
assets:
  download_external: true
  local_path: "assets/images"
  vendor_domains:
    - "framerusercontent.com"
    - "another-vendor.com"
```

### Attribute Replacements

Replace vendor-specific HTML attributes:

```yaml
attribute_replacements:
  - from: "data-framer-font-css"
    to: "data-font-css"
```

## What Gets Changed

### Removed Elements
- Vendor editor scripts (e.g., Framer editor bar)
- Generator meta tags
- Vendor-specific meta tags
- Template branding in titles/descriptions

### Updated Elements
- `<title>` - Personalized with your name
- Meta descriptions
- Open Graph (OG) tags
- Twitter Card tags
- Favicon links (downloaded locally)
- OG/Twitter images (downloaded locally)

### Preserved Elements
- All layout and styling
- JavaScript functionality
- CSS frameworks
- Font references (unless configured otherwise)

## File Structure

After running the script:

```
your-portfolio/
├── sanitize-template.py          # The script
├── sanitize-config.yml            # Your configuration
├── sanitization-report.txt        # Generated report
├── assets/
│   └── images/
│       ├── favicon-light.png      # Downloaded
│       ├── favicon-dark.png       # Downloaded
│       └── og-preview.png         # Downloaded
├── page.html                      # Updated
├── page.html.backup               # Backup
└── contact/
    ├── page.html                  # Updated
    └── page.html.backup           # Backup
```

## Safety Features

### Automatic Backups
Before modifying any file, a backup is created with `.backup` extension:
- `page.html` → `page.html.backup`

To restore:
```bash
mv page.html.backup page.html
```

### Dry Run Mode
Preview changes without modifying files:
```bash
python3 sanitize-template.py --dry-run
```

### Detailed Logging
All changes are logged to `sanitization-report.txt`:
- Files processed
- Elements removed
- Assets downloaded
- Errors encountered

## Common Use Cases

### 1. Clean Framer Template

```bash
# 1. Extract your Framer export
# 2. Edit sanitize-config.yml with your details
# 3. Run:
python3 sanitize-template.py
```

### 2. Clean Multiple Templates

```bash
# Process each template in separate directories
python3 sanitize-template.py --dir ./template1
python3 sanitize-template.py --dir ./template2
```

### 3. Custom Configuration Per Project

```bash
# Create project-specific configs
python3 sanitize-template.py --config project1-config.yml --dir ./project1
python3 sanitize-template.py --config project2-config.yml --dir ./project2
```

## Troubleshooting

### Missing Dependencies

Error: `ModuleNotFoundError: No module named 'bs4'`

Solution:
```bash
pip3 install beautifulsoup4 pyyaml
```

### Permission Errors

Error: `Permission denied`

Solution:
```bash
chmod +x sanitize-template.py
```

### Download Failures

If assets fail to download:
1. Check your internet connection
2. Verify the URLs are still valid
3. Check the error in `sanitization-report.txt`

### Encoding Issues

If you see garbled characters:
- The script uses UTF-8 encoding
- Make sure your HTML files are UTF-8 encoded

## Advanced Customization

### Adding Custom Removals

Edit `sanitize-config.yml`:

```yaml
remove_elements:
  - selector: "script"
    contains: "analytics.com"  # Remove analytics scripts
  - selector: "div.vendor-badge"  # Remove specific divs
```

### Custom Title Templates

```yaml
pages:
  case_studies:
    title_template: "{project_name} | Your Name | Portfolio"
    description_template: "View my {project_name} project..."
```

### Selective Asset Downloads

```yaml
assets:
  download_types:
    - "favicons"
    - "og_images"
    # Don't download twitter_images
```

## Contributing

Found a bug or have a feature request?
1. Check `sanitization-report.txt` for errors
2. Create a detailed issue description
3. Include your config file (remove personal info)

## License

Free to use and modify for your projects.

## Credits

Created to sanitize Framer/Resize templates and make them truly yours.

---

## Quick Reference

```bash
# Install dependencies
pip3 install beautifulsoup4 pyyaml

# Edit config
nano sanitize-config.yml

# Run script
python3 sanitize-template.py

# Check report
cat sanitization-report.txt

# Restore from backup if needed
mv page.html.backup page.html
```
