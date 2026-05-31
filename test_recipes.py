import pytest

from main import Ingredient, Recipe

def test_ingredient_creation():
    ingredient = Ingredient("Мука", 500, "г")
    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == 'г'

def test_ingredient_str():
    ingredient = Ingredient("Мука", 500, "г")
    assert str(ingredient) == "Мука: 500.0 г"

def test_ingredient_eq():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Мука", 100, "г")
    assert ingredient1 == ingredient2

    ingredient2 = Ingredient("Молоко", 500, "г")
    assert ingredient1 != ingredient2

    ingredient2 = Ingredient("Мука", 500, "кг")
    assert ingredient1 != ingredient2

def test_ingredient_quantity_must_be_positive():
    with pytest.raises(ValueError):
        Ingredient("Мука", 0, "г")

def test_recipe_creation():
    ingredient = Ingredient("Мука", 100, "г")
    recipe = Recipe("Панкейки", [ingredient])
    assert recipe.title == "Панкейки"
    assert recipe.ingredients == [ingredient]

def test_recipe_add_ingredient():
    ingredient = Ingredient("Мука", 100, "г")
    recipe = Recipe("Панкейки", [])
    recipe.add_ingredient(ingredient)
    assert len(recipe) == 1
    assert recipe.ingredients == [ingredient]

def test_recipe_add_existing_ingredient():
    recipe = Recipe("Панкейки", [Ingredient("Мука", 100, "г")])
    ingredient = Ingredient("Мука", 100, "г")
    recipe.add_ingredient(ingredient)
    assert len(recipe) == 1
    assert recipe.ingredients[0].name == "Мука"
    assert recipe.ingredients[0].quantity == 200.0
    assert recipe.ingredients[0].unit == "г"

def test_scale_returns_new_recipe():
    recipe = Recipe("Панкейки", [Ingredient("Мука", 100, "г")])
    scaled = recipe.scale(2)
    assert scaled is not recipe
    assert scaled.title == "Панкейки"
    assert scaled.ingredients[0].quantity == 200.0
    assert recipe.ingredients[0].quantity == 100.0

def test_recipe_scale_ratio():
    recipe = Recipe("Панкейки", [Ingredient("Мука", 100, "г")])
    with pytest.raises(ValueError):
        recipe.scale(0)

def test_recipe_len():
    recipe = Recipe("Панкейки",
                    [Ingredient("Мука", 100, "г"),
                                 Ingredient("Молоко", 500, "г")])
    assert len(recipe) == 2









