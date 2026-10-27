# kdp_category_picker

CLI tool for KDP authors to browse Amazon categories, validate category fit for a
book, save picks, and export them for KDP upload. Local-first — no accounts,
no API keys, no personal data.

## Features

- Browse Amazon KDP categories (browse, search, tree view)
- Save favorite category picks locally
- Validate category fit against book metadata (title, description, keywords)
- Export picks as a CSV ready for KDP upload
- No accounts, no API keys, nothing leaves your machine

## Install

```bash
pip install -e .
```

Or just run the module directly:

```bash
python -m kdp_category_picker.cli
```

## Quick start

```bash
# Browse top-level categories
kdp-cat browse

# Search categories by keyword
kdp-cat search fiction mystery

# See category tree under a path
kdp-cat tree "Computers & Technology"

# Save a pick
kdp-cat save "Computers & Technology > Programming > Programming Languages > Python"

# List your picks
kdp-cat picks

# Validate fit for a book
kdp-cat validate --title "The Massive AI Manual" --description "..." --keywords "ai,python"

# Export picks for KDP upload
kdp-cat export picks.csv
```

## Category fit rules

The built-in fit validator checks:

- Keyword overlap between the book and the category's typical keywords
- Title/subtitle keyword match
- Description keyword density
- Category depth (deeper, more specific categories score higher)
- Disallowed keyword presence (excludes adult, low-content, mismatched genres)

A score of 0–100 is returned with a recommendation (`fit`, `partial`, `poor`).

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC.

Built by **Asdale Dynamics, LLC** — beginner-friendly AI education, books, and
practical tools for authors and small businesses. Learn more at
dylanasdale.github.io.
