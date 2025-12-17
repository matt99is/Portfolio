# Template Sanitizer - Quick Start Guide

## 5-Minute Setup

### Step 1: Install Dependencies (30 seconds)

```bash
pip3 install -r requirements.txt
```

### Step 2: Edit Your Config (2 minutes)

Open `sanitize-config.yml` and update your personal info:

```yaml
personal:
  name: "Your Name Here"
  title: "Your Professional Title"
  description: "Your professional description..."
```

### Step 3: Run the Script (1 minute)

```bash
python3 sanitize-template.py
```

### Step 4: Review the Results

Check `sanitization-report.txt` to see what changed.

---

## What Just Happened?

The script just:
- ✅ Removed all "Framer" and "Resize" branding
- ✅ Updated page titles with your name
- ✅ Updated all meta descriptions
- ✅ Downloaded favicons and OG images locally
- ✅ Updated all image references to local paths
- ✅ Created backups of all modified files

---

## Before & After Example

### Before (Original Template)
```html
<title>Resize Light – Free Responsive Portfolio Template for Framer</title>
<meta name="generator" content="Framer 02004a2">
<link href="https://framerusercontent.com/images/favicon.png" rel="icon">
```

### After (Your Sanitized Version)
```html
<title>Your Name - Your Professional Title</title>
<link href="assets/images/favicon-light.png" rel="icon">
```

---

## File Structure After Running

```
your-portfolio/
├── assets/
│   └── images/
│       ├── favicon-light.png      ← Downloaded
│       ├── favicon-dark.png       ← Downloaded
│       └── og-preview.png         ← Downloaded
│
├── page.html                      ← Updated
├── page.html.backup               ← Original backup
├── contact/
│   ├── page.html                  ← Updated
│   └── page.html.backup           ← Original backup
│
└── sanitization-report.txt        ← What changed
```

---

## Next Steps

### Preview Your Site
Open `page.html` in a browser to see your changes.

### Restore if Needed
If something went wrong:
```bash
mv page.html.backup page.html
```

### Customize Further
Edit `sanitize-config.yml` to:
- Change which elements are removed
- Customize page titles
- Add more vendor domains to remove
- Configure asset downloads

---

## Common Customizations

### Change Contact Page Title
```yaml
pages:
  contact:
    title: "Get in Touch - Your Name"
    description: "Let's work together..."
```

### Add More Vendors to Remove
```yaml
assets:
  vendor_domains:
    - "framerusercontent.com"
    - "another-template-vendor.com"
```

### Don't Download Images (Keep External Links)
```yaml
assets:
  download_external: false
```

---

## Troubleshooting

**Script won't run?**
```bash
# Make it executable
chmod +x sanitize-template.py
```

**Missing dependencies?**
```bash
pip3 install beautifulsoup4 pyyaml
```

**Want to preview without changing files?**
```bash
python3 sanitize-template.py --dry-run
```

---

## Getting Help

1. Check `sanitization-report.txt` for errors
2. Read the full `SANITIZE-README.md`
3. Review your `sanitize-config.yml` settings

---

That's it! Your template is now sanitized and ready to deploy. 🎉
