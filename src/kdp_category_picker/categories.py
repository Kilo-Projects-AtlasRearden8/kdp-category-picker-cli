"""Amazon KDP category catalog (embedded, local-first, no API keys)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class Category:
    """A single Amazon KDP category node."""

    id: str
    name: str
    path: str  # full breadcrumb path, e.g. "Computers & Technology > Programming"
    keywords: tuple[str, ...]  # typical keywords associated with this category
    depth: int
    browse_nodes: tuple[str, ...] = ()  # Amazon browse node ids (illustrative)

    def matches(self, query: str) -> bool:
        q = query.lower()
        return (
            q in self.name.lower()
            or q in self.path.lower()
            or any(q in kw.lower() for kw in self.keywords)
        )


# Embedded category catalog. Paths use " > " as the breadcrumb separator.
# Keywords are representative terms a book in that category might use.
_CATEGORIES: List[Category] = [
    # Computers & Technology
    Category(
        id="comp-tech",
        name="Computers & Technology",
        path="Computers & Technology",
        keywords=("computer", "technology", "software", "hardware", "it", "tech"),
        depth=1,
    ),
    Category(
        id="comp-programming",
        name="Programming",
        path="Computers & Technology > Programming",
        keywords=("programming", "code", "coding", "developer", "software"),
        depth=2,
    ),
    Category(
        id="comp-python",
        name="Python",
        path="Computers & Technology > Programming > Programming Languages > Python",
        keywords=("python", "django", "flask", "pandas", "scripting"),
        depth=4,
    ),
    Category(
        id="comp-javascript",
        name="JavaScript",
        path="Computers & Technology > Programming > Programming Languages > JavaScript",
        keywords=("javascript", "js", "node", "react", "web development"),
        depth=4,
    ),
    Category(
        id="comp-ai",
        name="Artificial Intelligence",
        path="Computers & Technology > Programming > Artificial Intelligence",
        keywords=("ai", "artificial intelligence", "machine learning", "ml", "llm"),
        depth=3,
    ),
    Category(
        id="comp-local-ai",
        name="Local AI",
        path="Computers & Technology > Programming > Artificial Intelligence > Local AI",
        keywords=("local ai", "ollama", "local llm", "private ai", "run locally"),
        depth=4,
    ),
    Category(
        id="comp-web",
        name="Web Development",
        path="Computers & Technology > Programming > Web Development",
        keywords=("web", "html", "css", "frontend", "backend", "fullstack"),
        depth=3,
    ),
    # Business & Money
    Category(
        id="biz",
        name="Business & Money",
        path="Business & Money",
        keywords=("business", "money", "entrepreneur", "finance", "management"),
        depth=1,
    ),
    Category(
        id="biz-small-business",
        name="Small Business",
        path="Business & Money > Small Business & Entrepreneurship",
        keywords=("small business", "entrepreneurship", "startup", "llc"),
        depth=2,
    ),
    Category(
        id="biz-publishing",
        name="Self-Publishing",
        path="Business & Money > Small Business & Entrepreneurship > Self-Publishing",
        keywords=("self-publishing", "kdp", "kindle direct publishing", "author"),
        depth=3,
    ),
    # Health, Fitness & Dieting
    Category(
        id="health",
        name="Health, Fitness & Dieting",
        path="Health, Fitness & Dieting",
        keywords=("health", "fitness", "diet", "wellness", "nurse", "nursing"),
        depth=1,
    ),
    Category(
        id="health-nursing",
        name="Nursing",
        path="Health, Fitness & Dieting > Medical Books > Nursing",
        keywords=("nursing", "nurse", "rn", "patient care", "clinical"),
        depth=3,
    ),
    # Computers > AI > Healthcare AI (cross-cutting example)
    Category(
        id="comp-ai-healthcare",
        name="Healthcare AI",
        path="Computers & Technology > Programming > Artificial Intelligence > Healthcare AI",
        keywords=("healthcare ai", "medical ai", "ai for nurses", "clinical ai"),
        depth=4,
    ),
    # Fiction
    Category(
        id="fic",
        name="Literature & Fiction",
        path="Literature & Fiction",
        keywords=("fiction", "novel", "story", "literature"),
        depth=1,
    ),
    Category(
        id="fic-mystery",
        name="Mystery",
        path="Literature & Fiction > Mystery, Thriller & Suspense",
        keywords=("mystery", "thriller", "suspense", "detective", "crime"),
        depth=2,
    ),
    # Self-Help
    Category(
        id="self",
        name="Self-Help",
        path="Self-Help",
        keywords=("self-help", "productivity", "motivation", "adhd", "habits"),
        depth=1,
    ),
    Category(
        id="self-adhd",
        name="ADHD Productivity",
        path="Self-Help > ADHD & Productivity",
        keywords=("adhd", "low energy", "productivity", "executive function"),
        depth=2,
    ),
    # Gaming
    Category(
        id="game",
        name="Science Fiction & Fantasy > Gaming",
        path="Science Fiction & Fantasy > Gaming",
        keywords=("ffxiv", "final fantasy", "gaming", "mmo", "video games"),
        depth=2,
    ),
    Category(
        id="chess",
        name="Humor & Entertainment > Chess",
        path="Humor & Entertainment > Chess",
        keywords=("chess", "opening", "endgame", "grandmaster"),
        depth=2,
    ),
]


def list_categories() -> List[Category]:
    """Return all top-level categories."""
    seen: Dict[str, Category] = {}
    for cat in _CATEGORIES:
        top = cat.path.split(" > ")[0]
        seen.setdefault(top, cat)
    return list(seen.values())


def search_categories(query: str) -> List[Category]:
    """Return categories whose name, path, or keywords match the query."""
    return [cat for cat in _CATEGORIES if cat.matches(query)]


def get_category(category_id: str) -> Optional[Category]:
    """Return a category by id, or None if not found."""
    for cat in _CATEGORIES:
        if cat.id == category_id:
            return cat
    return None


def get_category_by_path(path: str) -> Optional[Category]:
    """Return a category by its full breadcrumb path."""
    for cat in _CATEGORIES:
        if cat.path == path:
            return cat
    return None


def tree_under(top: str) -> List[Category]:
    """Return all categories under a top-level path."""
    return [cat for cat in _CATEGORIES if cat.path.startswith(top + " > ") or cat.path == top]
