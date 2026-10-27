# STATUS

## What was built

A local-first Python CLI for KDP authors called `kdp-category-picker` (command:
`kdp-cat`). It lets authors browse Amazon Kindle Direct Publishing categories,
save category picks, validate how well a book fits a category, and export picks
as a CSV for KDP upload. No accounts, no API keys, no network calls, and no
personal data — everything runs offline on the author's machine.

### Components

- `src/kdp_category_picker/categories.py` — Embedded Amazon KDP category catalog
  (breadcrumbs, keywords, depth). Commands: `browse`, `search`, `tree`.
- `src/kdp_category_picker/fit.py` — Category fit validator scoring 0–100 with a
  `fit` / `partial` / `poor` recommendation based on keyword overlap, title
  match, description density, and category specificity, with a penalty for
  disallowed generic content (adult/low-content/etc.).
- `src/kdp_category_picker/store.py` — Local JSON picks store plus CSV export for
  KDP upload.
- `src/kdp_category_picker/cli.py` — argparse CLI entry point.
- `tests/test_fit.py` / `tests/test_cli.py` — Tests for fit rules and CLI.

### Packaging

- `pyproject.toml` — setuptools-based, registers the `kdp-cat` console script.
- MIT `LICENSE` (copyright: Asdale Dynamics, LLC).
- `README.md` — usage, features, credits.
- `.gitignore` — standard Python ignores.

## How to run

Install:

```bash
pip install -e .
```

(Requires Python 3.8+. `pip` may need `--break-system-packages` on externally
managed systems.)

Use:

```bash
# Browse top-level categories
kdp-cat browse

# Search categories
kdp-cat search python

# Show categories under a top-level path
kdp-cat tree "Computers & Technology"

# Save a pick (use ">" as breadcrumb separator)
kdp-cat save "Computers & Technology > Programming > Programming Languages > Python"

# List saved picks
kdp-cat picks

# Validate fit for a book
kdp-cat validate \
  --category "Computers & Technology > Programming > Programming Languages > Python" \
  --title "The Massive AI Manual" \
  --description "..." \
  --keywords "ai, python"

# Export picks to CSV for KDP upload
kdp-cat export picks.csv
```

Picks are stored at `~/.kdp_category_picker/picks.json` (overridable via the
store module).

## Verification results

- `python3 -m pytest -q` → **15 passed** (fit rules + CLI).
- `python3 -m build --wheel` → builds cleanly (wheel produced).
- `kdp-cat browse`, `search`, `tree`, `save`, `picks`, `validate`, `export` all
  exercised manually and produce expected output.

## Known gaps

- Category catalog is embedded and static (not scraped from Amazon); it covers a
  representative starter set, not the full Amazon taxonomy.
- Fit scoring is heuristic/keyword-based, not a guarantee of KDP acceptance.
- Export CSV is minimal (Category Path, Category ID, Note); KDP's bulk upload
  template may require additional columns.
- Picks store is a single local JSON file; no sync, encryption, or multi-user
  support (intentionally local-first).
- No code formatting/lint tooling configured yet (no ruff/black/flake8).

## Credits

Built by **Asdale Dynamics, LLC** — beginner-friendly AI education, books, and
practical tools for authors and small businesses. Learn more at
dylanasdale.github.io.

MIT License. Copyright (c) 2026 Asdale Dynamics, LLC.
