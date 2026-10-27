"""Category fit validation rules (no accounts, no API keys)."""

from __future__ import annotations

from dataclasses import dataclass

from .categories import Category


@dataclass
class FitResult:
    """Result of validating a book against a category."""

    score: int  # 0-100
    recommendation: str  # "fit", "partial", "poor"
    reasons: list[str]


# Keywords that suggest a book does NOT belong in a general/technical category.
DISALLOWED_GENERIC = ("adult", "erotica", "low content", "no content", "journal", "planner")

# Strong category-signal keywords weighted higher.
STRONG_SIGNALS = {
    "python": ("python", "django", "flask", "pandas"),
    "ai": ("ai", "artificial intelligence", "machine learning", "llm", "local ai", "ollama"),
    "nursing": ("nursing", "nurse", "rn", "patient care", "clinical"),
    "mystery": ("mystery", "thriller", "detective", "crime", "suspense"),
    "adhd": ("adhd", "executive function", "low energy", "productivity"),
    "chess": ("chess", "opening", "endgame", "grandmaster"),
    "gaming": ("ffxiv", "final fantasy", "mmo", "video games", "gaming"),
}


def _tokenize(text: str) -> list[str]:
    import re

    return [t for t in re.split(r"[^a-z0-9]+", text.lower()) if t]


def _keyword_overlap_score(text_tokens: list[str], category_keywords: tuple[str, ...]) -> int:
    """Score 0-40 based on keyword overlap between text and category keywords."""
    if not category_keywords:
        return 0
    hits = 0
    for kw in category_keywords:
        kw_tokens = _tokenize(kw)
        if not kw_tokens:
            continue
        if all(tok in text_tokens for tok in kw_tokens):
            hits += 1
    ratio = hits / len(category_keywords)
    return int(round(ratio * 40))


def _title_score(title_tokens: list[str], category_keywords: tuple[str, ...]) -> int:
    """Score 0-25 based on title keyword match."""
    if not category_keywords:
        return 0
    hits = sum(1 for kw in category_keywords if _tokenize(kw)[0] in title_tokens)
    ratio = hits / len(category_keywords)
    return int(round(ratio * 25))


def _description_score(desc_tokens: list[str], category_keywords: tuple[str, ...]) -> int:
    """Score 0-20 based on description keyword density."""
    if not category_keywords or not desc_tokens:
        return 0
    hits = sum(1 for kw in category_keywords if any(tok in desc_tokens for tok in _tokenize(kw)))
    ratio = hits / len(category_keywords)
    return int(round(min(ratio, 1.0) * 20))


def _depth_bonus(category: Category) -> int:
    """Deeper, more specific categories score higher (0-10)."""
    return min(category.depth * 2, 10)


def _disallowed_penalty(text: str) -> bool:
    """True if the book text contains disallowed generic keywords."""
    low = text.lower()
    return any(d in low for d in DISALLOWED_GENERIC)


def validate_fit(
    category: Category,
    title: str = "",
    description: str = "",
    keywords: str = "",
) -> FitResult:
    """Validate how well a book fits a category.

    Returns a FitResult with a 0-100 score and a recommendation.
    """
    combined_text = " ".join([title, description, keywords])
    text_tokens = _tokenize(combined_text)
    title_tokens = _tokenize(title)

    score = 0
    reasons: list[str] = []

    kw_score = _keyword_overlap_score(text_tokens, category.keywords)
    title_s = _title_score(title_tokens, category.keywords)
    desc_s = _description_score(text_tokens, category.keywords)
    depth_bonus = _depth_bonus(category)

    score += kw_score
    score += title_s
    score += desc_s
    score += depth_bonus

    if kw_score > 0:
        reasons.append(f"keyword overlap ({kw_score}/40)")
    if title_s > 0:
        reasons.append(f"title match ({title_s}/25)")
    if desc_s > 0:
        reasons.append(f"description match ({desc_s}/20)")
    if depth_bonus > 0:
        reasons.append(f"category specificity (+{depth_bonus}/10)")

    # Disallowed generic content penalizes heavily.
    if _disallowed_penalty(combined_text):
        score = int(score * 0.5)
        reasons.append("disallowed generic content detected (score halved)")

    score = max(0, min(100, score))

    if score >= 70:
        recommendation = "fit"
    elif score >= 40:
        recommendation = "partial"
    else:
        recommendation = "poor"

    return FitResult(score=score, recommendation=recommendation, reasons=reasons)
