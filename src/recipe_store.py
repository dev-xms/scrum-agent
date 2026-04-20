# backlog_id: BKI-001, BKI-002
import itertools


class RecipeStore:
    _id_counter = itertools.count(1)

    def __init__(self):
        self._recipes = []

    def add_recipe(self, title, ingredients, instructions):
        if not str(title).strip():
            raise ValueError("title required")
        if not str(ingredients).strip():
            raise ValueError("ingredients required")
        if not str(instructions).strip():
            raise ValueError("instructions required")
        self._recipes.append({
            "id": next(RecipeStore._id_counter),
            "title": title,
            "ingredients": ingredients,
            "instructions": instructions,
        })

    def get_recipes(self):
        return list(self._recipes)

    def delete_recipe(self, recipe_id):
        for i, r in enumerate(self._recipes):
            if r["id"] == recipe_id:
                self._recipes.pop(i)
                return
        raise KeyError(recipe_id)

    def filter_recipes(self, query):
        q = query.strip().lower()
        if not q:
            return self.get_recipes()
        return [r for r in self._recipes if q in r["title"].lower()]
