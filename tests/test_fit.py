"""Tests for category fit rules."""

import pytest

from kdp_category_picker import categories, fit


def _cat(path: str, keywords, depth: int = 2, name: str | None = None):
    import dataclasses

    return categories.Category(
        id="test-cat",
        name=name or path.split(" > ")[-1],
        path=path,
        keywords=tuple(keywords),
        depth=depth,
    )


def test_keyword_overlap_in_title():
    cat = _cat("Computers & Technology > Programming > Python", ("python", "django", "flask"))
    result = fit.validate_fit(cat, title="Learning Python Programming")
    assert result.score > 0
    assert result.recommendation in ("poor", "partial", "fit")


def test_full_metadata_reaches_fit():
    cat = _cat("Computers & Technology > Programming > Python", ("python", "django", "flask"))
    result = fit.validate_fit(
        cat,
        title="Learning Python Programming",
        description="A beginner guide to python, django and flask web development.",
        keywords="python, django, flask, programming",
    )
    assert result.recommendation == "fit"


def test_no_match_poor():
    cat = _cat("Computers & Technology > Programming > Python", ("python", "django"))
    result = fit.validate_fit(cat, title="Chicken Soup for the Soul")
    assert result.recommendation == "poor"
    assert result.score < 40


def test_deeper_category_scores_higher():
    shallow = _cat("Computers & Technology", ("python",), depth=1, name="Computers")
    deep = _cat("Computers & Technology > Programming > Python", ("python",), depth=4, name="Python")
    base = {"title": "Python", "description": "", "keywords": ""}
    assert (
        fit.validate_fit(deep, **base).score
        > fit.validate_fit(shallow, **base).score
    )


def test_disallowed_generic_halves_score():
    cat = _cat("Computers & Technology > Programming > Python", ("python",))
    clean = fit.validate_fit(cat, title="Python Basics").score
    tainted = fit.validate_fit(
        cat, title="Python Basics", description="this is a low content journal"
    ).score
    assert tainted <= clean


def test_strong_keywords_match():
    cat = _cat("Self-Help > ADHD & Productivity", ("adhd", "productivity"))
    result = fit.validate_fit(
        cat, title="ADHD Productivity for Nurses", description="low energy productivity tips"
    )
    assert result.recommendation == "fit"
    assert result.score >= 70


def test_description_density_boosts_score():
    cat = _cat("Health, Fitness & Dieting > Nursing", ("nursing", "nurse", "patient care"))
    no_desc = fit.validate_fit(cat, title="Nursing", description="", keywords="").score
    with_desc = fit.validate_fit(
        cat,
        title="Nursing",
        description="patient care and nursing practice for registered nurses",
        keywords="nursing, rn, clinical",
    ).score
    assert with_desc > no_desc


def test_score_bounded_0_to_100():
    cat = _cat("Computers & Technology > Programming > Python", ("python",))
    for title in ["Python Python Python Python Python Python", ""]:
        result = fit.validate_fit(cat, title=title)
        assert 0 <= result.score <= 100


def test_recommendation_thresholds():
    cat = _cat("Computers & Technology > Programming > Python", ("python",))
    good = fit.validate_fit(cat, title="Python Programming Guide", keywords="python, django")
    assert good.recommendation == "fit"
    poor = fit.validate_fit(cat, title="Cooking Recipes")
    assert poor.recommendation == "poor"
