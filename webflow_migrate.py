#!/usr/bin/env python3
"""
Webflow CMS migration script.
- Archives existing CMS content
- Creates new Work and Writing items from markdown source files
- Deletes template items
"""

import os
import re
import json
import urllib.request
import urllib.error

# ─── Config ─────────────────────────────────────────────────────────────────

API_TOKEN = os.environ["WEBFLOW_API_TOKEN"]
SITE_ID = os.environ["WEBFLOW_SITE_ID"]
WORK_COLLECTION = "69ac1b62b6801fd3e014b5b7"
WRITING_COLLECTION = "69ac1b62b6801fd3e014b5d8"

BASE_URL = "https://api.webflow.com/v2"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "accept": "application/json",
}

ARCHIVE_PATH = "/home/matt99is/projects/Portfolio/archive/cms-backup.json"

# ─── HTTP helpers ────────────────────────────────────────────────────────────

def api(method, path, body=None):
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            raw = resp.read()
            return json.loads(raw) if raw.strip() else {"ok": True}
    except urllib.error.HTTPError as e:
        err = e.read().decode()
        print(f"  HTTP {e.code} on {method} {path}: {err}")
        return None

# ─── Markdown → HTML ─────────────────────────────────────────────────────────

def md_to_html(text):
    """Simple markdown-to-HTML converter for the subset used in these files."""
    lines = text.split("\n")
    html_parts = []
    in_table = False
    table_rows = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Skip image/link placeholders
        if re.match(r'^\[IMAGE:', line) or re.match(r'^\[LINK:', line):
            i += 1
            continue

        # Headings
        if line.startswith("### "):
            html_parts.append(f'<h3>{inline_md(line[4:])}</h3>')
        elif line.startswith("## "):
            html_parts.append(f'<h2>{inline_md(line[3:])}</h2>')
        elif line.startswith("# "):
            html_parts.append(f'<h1>{inline_md(line[2:])}</h1>')

        # Horizontal rule
        elif line.strip() in ("---", "***", "___"):
            i += 1
            continue  # skip dividers

        # Table detection
        elif "|" in line and line.strip().startswith("|"):
            table_rows.append(line)
            in_table = True

        # After table rows, flush table when non-table line hit
        else:
            if in_table and table_rows:
                html_parts.append(render_table(table_rows))
                table_rows = []
                in_table = False

            # Bullet list
            if line.startswith("- "):
                items = []
                while i < len(lines) and lines[i].startswith("- "):
                    items.append(f'<li>{inline_md(lines[i][2:])}</li>')
                    i += 1
                html_parts.append("<ul>" + "".join(items) + "</ul>")
                continue

            # Blockquote
            elif line.startswith("> "):
                html_parts.append(f'<blockquote><p>{inline_md(line[2:])}</p></blockquote>')

            # Empty line — paragraph break (ignore)
            elif line.strip() == "":
                pass

            # Normal paragraph
            else:
                html_parts.append(f'<p>{inline_md(line)}</p>')

        i += 1

    # Flush any remaining table
    if table_rows:
        html_parts.append(render_table(table_rows))

    return "\n".join(html_parts)


def inline_md(text):
    """Convert inline markdown: bold, italic, code."""
    # Bold+italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Code
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    return text


def render_table(rows):
    """Convert markdown table rows to HTML table."""
    html = ["<table>"]
    for idx, row in enumerate(rows):
        if re.match(r'^\|[-| ]+\|$', row.strip()):
            continue  # separator row
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        tag = "th" if idx == 0 else "td"
        html.append("<tr>" + "".join(f"<{tag}>{inline_md(c)}</{tag}>" for c in cells) + "</tr>")
    html.append("</table>")
    return "\n".join(html)


# ─── Content extraction ───────────────────────────────────────────────────────

def read_file(path):
    with open(path) as f:
        return f.read()


def extract_frontmatter_html(text):
    """Extract the opening paragraph and the **What/Role/Timeline/Outcome block as HTML."""
    lines = text.split("\n")
    # Skip h1 title line, grab subtitle, skip ---, then grab **key:** value lines
    i = 0
    subtitle = ""
    meta_lines = []

    while i < len(lines):
        line = lines[i]
        if line.startswith("# "):
            i += 1
            # Next non-empty line is subtitle
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            if i < len(lines) and not lines[i].startswith("---") and not lines[i].startswith("**"):
                subtitle = lines[i].strip()
            i += 1
            continue
        if line.strip() == "---":
            # Collect meta lines until next ---
            i += 1
            while i < len(lines) and lines[i].strip() != "---":
                if lines[i].strip():
                    meta_lines.append(lines[i].strip())
                i += 1
            break
        i += 1

    parts = []
    if subtitle:
        parts.append(f"<p><em>{inline_md(subtitle)}</em></p>")
    if meta_lines:
        parts.append("<ul>")
        for ml in meta_lines:
            parts.append(f"<li>{inline_md(ml)}</li>")
        parts.append("</ul>")

    return "\n".join(parts)


def extract_body_sections(text, outcome_heading=None):
    """
    Split main body into process and outcome sections.
    outcome_heading: first ## heading that begins the outcome section.
    Returns (process_html, outcome_html)
    """
    # Strip frontmatter (title, subtitle, ---, meta, ---)
    # Find second --- and take everything after
    parts = text.split("---")
    # parts[0] = title+subtitle, parts[1] = meta block, parts[2:] = body
    body = "---".join(parts[2:]).strip() if len(parts) > 2 else text

    if not outcome_heading:
        return md_to_html(body), ""

    # Split at the outcome heading
    pattern = rf'(^|\n)(## {re.escape(outcome_heading)})'
    match = re.search(pattern, body)
    if match:
        process = body[:match.start()].strip()
        outcome = body[match.start():].strip()
        return md_to_html(process), md_to_html(outcome)
    else:
        return md_to_html(body), ""


def extract_blog_html(text):
    """Convert entire blog post to HTML, skipping title."""
    lines = text.split("\n")
    # Skip title (first # line) and subtitle block before ---
    i = 0
    while i < len(lines) and not lines[i].strip() == "---":
        i += 1
    # Skip the --- and empty lines
    i += 1
    while i < len(lines) and lines[i].strip() == "":
        i += 1
    body = "\n".join(lines[i:])
    return md_to_html(body)


# ─── Main migration ───────────────────────────────────────────────────────────

def main():
    print("=== Webflow CMS Migration ===\n")

    # Step 1: Archive existing content
    print("1. Archiving existing CMS content...")
    work_items = api("GET", f"/collections/{WORK_COLLECTION}/items")
    writing_items = api("GET", f"/collections/{WRITING_COLLECTION}/items")
    archive = {"work": work_items, "writing": writing_items}
    os.makedirs(os.path.dirname(ARCHIVE_PATH), exist_ok=True)
    with open(ARCHIVE_PATH, "w") as f:
        json.dump(archive, f, indent=2)
    print(f"   Saved to {ARCHIVE_PATH}")
    print(f"   Work items: {len(work_items['items'])}, Writing items: {len(writing_items['items'])}\n")

    # Collect template item IDs for deletion later
    work_ids_to_delete = [item["id"] for item in work_items["items"]]
    writing_ids_to_delete = [item["id"] for item in writing_items["items"]]

    base = "/home/matt99is/projects/Portfolio/case-studies"

    # ── Step 2: Create Work items ─────────────────────────────────────────────

    print("2. Creating Work items...\n")

    # Item 1: Minibasket
    print("   Creating: Minibasket Modal...")
    text1 = read_file(f"{base}/01-minibasket.md")
    overview1 = extract_frontmatter_html(text1)
    process1, outcome1 = extract_body_sections(
        text1, outcome_heading="Shipped in a month"
    )
    r1 = api("POST", f"/collections/{WORK_COLLECTION}/items", {
        "isArchived": False,
        "isDraft": False,
        "fieldData": {
            "name": "Increasing AOV by 4.4% Through a High-Intent Touchpoint",
            "slug": "minibasket-redesign",
            "order": 1,
            "title": "Increasing AOV by 4.4% Through a High-Intent Touchpoint",
            "description": "A focused intervention at the moment of commitment. From proposal to production in one month.",
            "my-role": "UX Designer",
            "core-team": "UX Design\nPrototyping\nUser Research\nAccessibility Testing",
            "date": "1 Month",
            "the-brief-3": overview1,
            "the-process-3": process1,
            "the-outcome-3": outcome1,
            "hide": False,
        }
    })
    minibasket_id = r1["id"] if r1 else None
    print(f"   {'OK' if r1 else 'FAILED'}: {minibasket_id or 'error'}")

    # Item 2: Basket Redesign
    print("   Creating: Basket Page Redesign...")
    text2 = read_file(f"{base}/02-basket-redesign.md")
    overview2 = extract_frontmatter_html(text2)
    process2, outcome2 = extract_body_sections(
        text2, outcome_heading="Approved and moving into delivery"
    )
    r2 = api("POST", f"/collections/{WORK_COLLECTION}/items", {
        "isArchived": False,
        "isDraft": False,
        "fieldData": {
            "name": "Quantifying a Problem Nobody Was Looking At",
            "slug": "basket-redesign",
            "order": 2,
            "title": "Quantifying a Problem Nobody Was Looking At",
            "description": "How I identified a high-impact revenue problem through behaviour data, built the business case from scratch, and designed the solution.",
            "my-role": "UX Designer",
            "core-team": "Baymard Audit\nCompetitor Analysis\nUser Research\nPrototyping",
            "date": "3 Months (in engineering delivery)",
            "the-brief-3": overview2,
            "the-process-3": process2,
            "the-outcome-3": outcome2,
            "hide": False,
        }
    })
    basket_id = r2["id"] if r2 else None
    print(f"   {'OK' if r2 else 'FAILED'}: {basket_id or 'error'}")

    # Item 3: ACE Platform
    print("   Creating: ACE Enterprise Platform...")
    text3 = read_file(f"{base}/03-ace-platform.md")
    overview3 = extract_frontmatter_html(text3)
    process3, outcome3 = extract_body_sections(
        text3, outcome_heading="Five years of learning"
    )
    r3 = api("POST", f"/collections/{WORK_COLLECTION}/items", {
        "isArchived": False,
        "isDraft": False,
        "fieldData": {
            "name": "Replacing Five Systems with One Device for 5,000 Store Colleagues",
            "slug": "ace-device",
            "order": 3,
            "title": "Replacing Five Systems with One Device for 5,000 Store Colleagues",
            "description": "Five years as sole designer on an award-winning enterprise platform deployed across 450+ stores.",
            "my-role": "Sole UX Designer",
            "core-team": "Navigation Architecture\nInformation Hierarchy\nDesign System\n15+ Features",
            "date": "5 Years (ongoing)",
            "the-brief-3": overview3,
            "the-process-3": process3,
            "the-outcome-3": outcome3,
            "hide": False,
        }
    })
    ace_id = r3["id"] if r3 else None
    print(f"   {'OK' if r3 else 'FAILED'}: {ace_id or 'error'}")

    # ── Step 3: Create Writing item ───────────────────────────────────────────

    print("\n3. Creating Writing item...\n")

    text4 = read_file(f"{base}/04-ai-analysis-tool-blog.md")
    article_html = extract_blog_html(text4)
    r4 = api("POST", f"/collections/{WRITING_COLLECTION}/items", {
        "isArchived": False,
        "isDraft": False,
        "fieldData": {
            "name": "How I Built a Competitive Analysis Tool with AI",
            "slug": "competitive-analysis-tool-ai",
            "article-summary": "What started as a quick fix for a single project has become a production tool I continue to develop and use.",
            "date": "2025-11-24T00:00:00.000Z",
            "minute-read": 5,
            "article": article_html,
        }
    })
    blog_id = r4["id"] if r4 else None
    print(f"   {'OK' if r4 else 'FAILED'}: {blog_id or 'error'}")

    # ── Step 4: Delete template Work items ────────────────────────────────────

    print("\n4. Clearing cross-references on template Work items...")
    for item_id in work_ids_to_delete:
        api("PATCH", f"/collections/{WORK_COLLECTION}/items/{item_id}", {
            "fieldData": {"next": None}
        })

    print("   Clearing cross-references on template Writing items...")
    for item_id in writing_ids_to_delete:
        api("PATCH", f"/collections/{WRITING_COLLECTION}/items/{item_id}", {
            "fieldData": {"next-article": None}
        })

    print("\n5. Deleting template Work items...")
    for item_id in work_ids_to_delete:
        result = api("DELETE", f"/collections/{WORK_COLLECTION}/items/{item_id}")
        status = "OK" if result is not None else "FAILED"
        print(f"   {status}: deleted Work {item_id}")

    print("\n6. Deleting template Writing items...")
    for item_id in writing_ids_to_delete:
        result = api("DELETE", f"/collections/{WRITING_COLLECTION}/items/{item_id}")
        status = "OK" if result is not None else "FAILED"
        print(f"   {status}: deleted Writing {item_id}")

    # ── Summary ───────────────────────────────────────────────────────────────

    print("\n=== Summary ===")
    print(f"Work items created: {sum(1 for x in [minibasket_id, basket_id, ace_id] if x)}/3")
    print(f"Writing items created: {sum(1 for x in [blog_id] if x)}/1")
    print(f"Template Work items deleted: {len(work_ids_to_delete)}")
    print(f"Template Writing items deleted: {len(writing_ids_to_delete)}")
    print(f"\nNew IDs:")
    print(f"  Minibasket: {minibasket_id}")
    print(f"  Basket Redesign: {basket_id}")
    print(f"  ACE Platform: {ace_id}")
    print(f"  AI Blog Post: {blog_id}")
    print("\nNote: Images, static page content, social links, and footer")
    print("require Webflow Designer access (not available via CMS API).")


if __name__ == "__main__":
    main()
