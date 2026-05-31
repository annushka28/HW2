from pandas.core.dtypes.inference import is_float
from sympy.physics.units.util import quantity_simplify

class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Количество должно быть положительным")
        self._quantity = value

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"

    def __eq__(self, other):
        return self.name == other.name and self.unit == other.unit



class Recipe:
    def __init__(self, title, ingredients):
        self.title = title
        self.ingredients = []
        for ingredient in ingredients:
            self.add_ingredient(ingredient)

    def add_ingredient(self, ingredient):
        for i in self.ingredients:
            if i == ingredient:
                i.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    @staticmethod
    def is_valid_ratio(ratio):
        return isinstance(ratio, (int, float)) and ratio > 0

    def scale(self, ratio):
        if not self.is_valid_ratio(ratio):
            raise ValueError("Коэффицент должен быть положительным")

        edit_ingredients = []
        for i in self.ingredients:
            edit_ingredients.append(Ingredient(i.name, i.quantity * ratio, i.unit))

        return Recipe(self.title, edit_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        s = f"{self.title} \nСписок ингредиентов:"
        for i in self.ingredients:
            s += "\n"+str(i)
        return s


class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        if ingredients is None:
            ingredients = []
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio):
        edit_recipe = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, edit_recipe.ingredients)

    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"


class ShoppingList:
    def __init__(self):
        self._items = []

    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        edit_recipe = recipe.scale(portions)
        for i in edit_recipe.ingredients:
            self._items.append((i, recipe.title))

    def remove_recipe(self, title):
        new_items = []
        for i, recipe_title in self._items:
            if recipe_title != title:
                new_items.append((i, recipe_title))
        self._items = new_items

    def get_list(self):
        ingredients_sum = {}
        for i, r_title in self._items:
            key = (i.name, i.unit)
            if key in ingredients_sum:
                ingredients_sum[key] += i.quantity
            else:
                ingredients_sum[key] = i.quantity

        res = []
        for (name, unit), quantity in ingredients_sum.items():
            res.append(Ingredient(name, quantity, unit))
        res.sort(key = lambda i: i.name)
        return res

    def __add__(self, other):
        new_shopping_list = ShoppingList()
        new_shopping_list._items = self._items + other._items
        return new_shopping_list









