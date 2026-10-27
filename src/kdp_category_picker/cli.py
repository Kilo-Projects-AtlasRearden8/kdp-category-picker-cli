"""Command-line interface for kdp_category_picker."""

from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from . import categories, fit, store


def _fmt_cat(cat: categories.Category, indent: int = 0) -> str:
    prefix = "  " * indent
    return f"{prefix}{cat.name}  ({cat.path})"


def cmd_browse(args: argparse.Namespace) -> int:
    cats = categories.list_categories()
    if not cats:
        print("No categories found.")
        return 0
    print("Top-level Amazon KDP categories:")
    for cat in cats:
        print(f"  - {cat.name}")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    query = " ".join(args.query)
    results = categories.search_categories(query)
    if not results:
        print(f"No categories matched '{query}'.")
        return 0
    print(f"Categories matching '{query}':")
    for cat in results:
        print(f"  - {_fmt_cat(cat)}")
    return 0


def cmd_tree(args: argparse.Namespace) -> int:
    top = args.path
    results = categories.tree_under(top)
    if not results:
        print(f"No categories found under '{top}'.")
        return 0
    print(f"Categories under '{top}':")
    for cat in results:
        print(f"  - {_fmt_cat(cat, indent=1)}")
    return 0


def cmd_save(args: argparse.Namespace) -> int:
    # Reconstruct breadcrumb: join args, split on ">", strip segments.
    full = " ".join(args.path)
    parts = [seg.strip() for seg in full.split(">") if seg.strip()]
    path = " > ".join(parts)
    cat = categories.get_category_by_path(path)
    if cat is None:
        # Try by id
        cat = categories.get_category(path)
    if cat is None:
        print(f"Category not found: {path}")
        return 1
    st = store.get_store()
    if st.add(cat, note=args.note or ""):
        print(f"Saved: {cat.path}")
    else:
        print(f"Already saved: {cat.path}")
    return 0


def cmd_picks(args: argparse.Namespace) -> int:
    st = store.get_store()
    picks = st.list()
    if not picks:
        print("No saved picks.")
        return 0
    print("Saved category picks:")
    for i, p in enumerate(picks, 1):
        note = f"  [{p.note}]" if p.note else ""
        print(f"  {i}. {p.category_path}{note}")
    return 0


def cmd_remove(args: argparse.Namespace) -> int:
    st = store.get_store()
    if st.remove(args.category_id):
        print(f"Removed pick: {args.category_id}")
    else:
        print(f"No pick found for: {args.category_id}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    # Resolve category
    cat: Optional[categories.Category] = None
    if args.category:
        cat = categories.get_category_by_path(args.category) or categories.get_category(args.category)
    if cat is None:
        print("Category not specified or not found. Use --category.")
        return 1

    result = fit.validate_fit(
        cat,
        title=args.title or "",
        description=args.description or "",
        keywords=args.keywords or "",
    )
    print(f"Category: {cat.path}")
    print(f"Fit score: {result.score}/100")
    print(f"Recommendation: {result.recommendation}")
    if result.reasons:
        print("Reasons:")
        for r in result.reasons:
            print(f"  - {r}")
    return 0


def cmd_export(args: argparse.Namespace) -> int:
    st = store.get_store()
    out = args.output
    st.export_csv(out)
    print(f"Exported {len(st.list())} picks to {out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kdp-cat",
        description="Browse Amazon KDP categories, validate fit, and export picks.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("browse", help="List top-level categories").set_defaults(func=cmd_browse)

    p_search = sub.add_parser("search", help="Search categories by keyword")
    p_search.add_argument("query", nargs="+", help="Keyword(s) to search")
    p_search.set_defaults(func=cmd_search)

    p_tree = sub.add_parser("tree", help="List categories under a path")
    p_tree.add_argument("path", help="Top-level category path")
    p_tree.set_defaults(func=cmd_tree)

    p_save = sub.add_parser("save", help="Save a category pick")
    p_save.add_argument("path", nargs="+", help="Category breadcrumb path (words separated by spaces)")
    p_save.add_argument("--note", default="", help="Optional note for the pick")
    p_save.set_defaults(func=cmd_save)

    sub.add_parser("picks", help="List saved picks").set_defaults(func=cmd_picks)

    p_rm = sub.add_parser("remove", help="Remove a saved pick by category id")
    p_rm.add_argument("category_id", help="Category id to remove")
    p_rm.set_defaults(func=cmd_remove)

    p_val = sub.add_parser("validate", help="Validate category fit for a book")
    p_val.add_argument("--category", required=True, help="Category path or id")
    p_val.add_argument("--title", default="", help="Book title")
    p_val.add_argument("--description", default="", help="Book description")
    p_val.add_argument("--keywords", default="", help="Comma-separated keywords")
    p_val.set_defaults(func=cmd_validate)

    p_exp = sub.add_parser("export", help="Export picks to CSV for KDP upload")
    p_exp.add_argument("output", help="Output CSV path")
    p_exp.set_defaults(func=cmd_export)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
