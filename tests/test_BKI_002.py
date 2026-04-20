"""
BKI-002: The Smart Plate — Sprint 2 Unit Tests (pytest)
Covers: US.4 (search by name), US.6 (dark mode — logic layer N/A, UI-only)
Target module: src/recipe_store.py :: filter_recipes()
"""
import pytest
from src.recipe_store import RecipeStore


@pytest.fixture
def store():
    s = RecipeStore()
    s.add_recipe("Pasta Bolognese", "Noodles, beef", "Boil and mix")
    s.add_recipe("Chicken Soup", "Chicken, water", "Simmer")
    s.add_recipe("Pasta Carbonara", "Noodles, egg", "Toss")
    return s


# --- US.4: Search Recipes by Name ---

def test_us4_search_partial_match(store):
    """Partial title match returns matching recipes only."""
    results = store.filter_recipes("pasta")
    assert len(results) == 2
    titles = [r["title"] for r in results]
    assert "Pasta Bolognese" in titles
    assert "Pasta Carbonara" in titles


def test_us4_search_case_insensitive(store):
    """Search is case-insensitive."""
    assert len(store.filter_recipes("PASTA")) == 2
    assert len(store.filter_recipes("Pasta")) == 2
    assert len(store.filter_recipes("pAsTA")) == 2


def test_us4_search_no_match_returns_empty(store):
    """Query with no match returns empty list."""
    results = store.filter_recipes("pizza")
    assert results == []


def test_us4_search_empty_query_returns_all(store):
    """Empty query returns all recipes."""
    results = store.filter_recipes("")
    assert len(results) == 3


def test_us4_search_whitespace_query_returns_all(store):
    """Whitespace-only query treated as empty — returns all."""
    results = store.filter_recipes("   ")
    assert len(results) == 3


def test_us4_search_exact_match(store):
    """Exact title match returns single recipe."""
    results = store.filter_recipes("Chicken Soup")
    assert len(results) == 1
    assert results[0]["title"] == "Chicken Soup"


def test_us4_search_does_not_match_ingredients(store):
    """Search only matches title, not ingredients."""
    results = store.filter_recipes("beef")
    assert results == []


def test_us4_search_empty_store(store):
    """Search on empty store returns empty list."""
    empty = RecipeStore()
    assert empty.filter_recipes("pasta") == []
