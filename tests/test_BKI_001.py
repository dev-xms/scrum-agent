"""
BKI-001: The Smart Plate — Sprint 1 Unit Tests (pytest)
Covers: US.1 (save), US.2 (view list), US.3 (delete)
Target module: src/recipe_store.py
"""
import pytest
from src.recipe_store import RecipeStore


@pytest.fixture
def store():
    return RecipeStore()


# --- US.1: Save Recipe ---

def test_us1_save_recipe_persists(store):
    """Given valid fields, recipe saved and retrievable."""
    store.add_recipe("Pasta", "Noodles, sauce", "Boil and mix")
    recipes = store.get_recipes()
    assert len(recipes) == 1
    assert recipes[0]["title"] == "Pasta"
    assert recipes[0]["ingredients"] == "Noodles, sauce"
    assert recipes[0]["instructions"] == "Boil and mix"


def test_us1_save_recipe_assigns_id(store):
    """Each saved recipe gets unique id."""
    store.add_recipe("A", "i", "s")
    store.add_recipe("B", "i", "s")
    ids = [r["id"] for r in store.get_recipes()]
    assert ids[0] != ids[1]


def test_us1_empty_title_raises(store):
    """Given empty title, add_recipe raises ValueError."""
    with pytest.raises(ValueError):
        store.add_recipe("", "ingredients", "instructions")


def test_us1_whitespace_title_raises(store):
    """Whitespace-only title treated as empty."""
    with pytest.raises(ValueError):
        store.add_recipe("   ", "ingredients", "instructions")


def test_us1_empty_ingredients_raises(store):
    with pytest.raises(ValueError):
        store.add_recipe("Title", "", "instructions")


def test_us1_empty_instructions_raises(store):
    with pytest.raises(ValueError):
        store.add_recipe("Title", "ingredients", "")


def test_us1_invalid_save_does_not_persist(store):
    """Failed save leaves store unchanged."""
    with pytest.raises(ValueError):
        store.add_recipe("", "i", "s")
    assert store.get_recipes() == []


# --- US.2: View Recipe List ---

def test_us2_get_recipes_returns_all(store):
    """All saved recipes returned."""
    store.add_recipe("A", "i", "s")
    store.add_recipe("B", "i", "s")
    assert len(store.get_recipes()) == 2


def test_us2_empty_store_returns_empty_list(store):
    """No recipes saved → empty list."""
    assert store.get_recipes() == []


def test_us2_recipe_titles_visible(store):
    """Each recipe in list exposes title field."""
    store.add_recipe("Salad", "Lettuce", "Toss")
    recipes = store.get_recipes()
    assert "title" in recipes[0]


# --- US.3: Delete Recipe ---

def test_us3_delete_removes_recipe(store):
    """Delete by id removes recipe from store."""
    store.add_recipe("Soup", "Water", "Boil")
    rid = store.get_recipes()[0]["id"]
    store.delete_recipe(rid)
    assert store.get_recipes() == []


def test_us3_delete_only_removes_target(store):
    """Delete removes only the targeted recipe."""
    store.add_recipe("A", "i", "s")
    store.add_recipe("B", "i", "s")
    rid = store.get_recipes()[0]["id"]
    store.delete_recipe(rid)
    remaining = store.get_recipes()
    assert len(remaining) == 1
    assert remaining[0]["title"] == "B"


def test_us3_delete_nonexistent_raises(store):
    """Deleting unknown id raises KeyError."""
    with pytest.raises(KeyError):
        store.delete_recipe(99999)
