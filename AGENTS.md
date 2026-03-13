# AGENTS.md

This is the entry point for any AI agent working on this project. Read this file first, then follow the load order before touching files.

---

## What this project is

Portfolio is a content-and-assets repository for a UX portfolio workflow. It stores case study markdown, static assets served through jsDelivr/Netlify, and redirect config supporting external publishing.

**Stack:** Markdown content, static assets, Netlify redirects, Webflow-integrated publishing workflow

---

## Load order

Read these files before starting any task:

| Priority | File | Why |
|---|---|---|
| 1 - always | `case-studies/homepage.md` | Homepage content source |
| 2 - always | `case-studies/about.md` | About-page content source |
| 3 - before frontend work | `/home/matt99is/projects/vault/Patterns/frontend-standards.md` | Before any frontend or UI work |
| 3 - for portfolio case updates | `case-studies/01-minibasket.md` | Representative long-form case study format |
| 4 - for routing behavior | `_redirects` | Netlify redirect rules |
| 5 - for deploy behavior | `netlify.toml` | Netlify serving configuration |

---

## Startup Gate (Mandatory)

Before running commands, searching files, or editing content, every agent must:

1. Read this `AGENTS.md`.
2. Read `case-studies/homepage.md`.
3. Read `case-studies/about.md`.
4. Read vault project note: `/home/matt99is/projects/vault/Projects/Portfolio.md`.
5. Read vault governance note: `/home/matt99is/projects/vault/Patterns/vault-note-governance.md`.
6. In the first response of the session, explicitly confirm these files were loaded.

If any step is missed, stop and complete it before continuing.

---

## Vault Note Contract (Anti-Bloat)

The vault project note at `/home/matt99is/projects/vault/Projects/Portfolio.md` is startup memory, not history.

### Fixed purpose
- Keep only current operating truth needed to start work quickly.
- Keep active decisions, current gotchas, and near-term next steps.
- Do not use it as a changelog, release log, or commit diary.

### Hard limits
- Max 220 lines.
- Max 14,000 characters.
- Required `##` sections:
  - `What it is`
  - `Current status`
  - `Active decisions`
  - `Known gotchas`
  - `Next steps`
  - `References`
- Bullet caps:
  - `Current status`: 12 bullets max
  - `Active decisions`: 8 bullets max
  - `Known gotchas`: 8 bullets max
  - `Next steps`: 6 bullets max
  - `References`: 12 bullets max

### Update rule
- Replace existing bullets when state changes; do not append chronological entries.
- Keep one bullet per capability/state, written as present tense current truth.

### Archive policy
- Default: no rolling archive notes.
- Optional: one manual snapshot before major rewrites, only on explicit user request.

---

## Key commands

```bash
# Static preview
python3 -m http.server 8787

# Validate key content files are present
ls case-studies/
```

---

## Critical gotchas

- This repo is not the full Webflow source; it supports content/assets feeding external publishing.
- `.env` may contain Webflow credentials locally; never commit or print secrets.
- Public image URLs are expected to remain stable for jsDelivr; avoid breaking `images/` paths.
- `_redirects` changes can break CV/document routes; test redirects after edits.

---

## Repo structure

```
AGENTS.md
case-studies/               # Source markdown for pages and case studies
images/                     # Public assets (CV/docs/images)
_redirects                  # Netlify redirect rules
netlify.toml
```
