import pytest

from main import Ingredient, Recipe, ShoppingList


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
                                 Ingredient("Молоко", 200, "мл")])
    assert len(recipe) == 2

def test_shopping_list_add_recipe():
    recipe = Recipe("Панкейки", [Ingredient("Мука", 100, "г"), Ingredient("Молоко", 200, "мл")])
    shopping = ShoppingList()
    shopping.add_recipe(recipe, 2)
    res = shopping.get_list()
    assert len(res) == 2
    assert res[0].name == "Молоко"
    assert res[0].quantity == 400.0
    assert res[1].name == "Мука"
    assert res[1].quantity == 200.0

def test_shopping_list_add_recipe_portions():
    recipe = Recipe("Панкейки", [Ingredient("Мука", 100, "г")])
    shopping = ShoppingList()
    with pytest.raises(ValueError):
        shopping.add_recipe(recipe, 0)

def test_shopping_list_remove_recipe():
    pancakes = Recipe("Панкейки", [Ingredient("Мука", 100, "г")])
    cake = Recipe("Торт",[Ingredient("Сахар", 100, "г")])
    shopping = ShoppingList()
    shopping.add_recipe(pancakes,1)
    shopping.add_recipe(cake, 1)
    shopping.remove_recipe("Панкейки")
    res = shopping.get_list()
    assert len(res) == 1
    assert res[0].name == "Сахар"

def test_shopping_list_remove_recipe_nothing():
    recipe = Recipe("Панкейки", [Ingredient("Мука", 100, "г")])
    shopping = ShoppingList()
    shopping.add_recipe(recipe, 1)
    shopping.remove_recipe("Торт")
    res = shopping.get_list()
    assert len(res) == 1
    assert res[0].name == "Мука"
    assert res[0].quantity == 100.0

def test_shopping_list_get_list_similars():
    pancakes1 = Recipe("Панкейки", [Ingredient("Мука", 100, "г")])
    pancakes2 = Recipe("Панкейки", [Ingredient("Мука", 50, "г")])
    shopping = ShoppingList()
    shopping.add_recipe(pancakes1, 1)
    shopping.add_recipe(pancakes2, 1)
    res = shopping.get_list()
    assert len(res) == 1
    assert res[0].name == "Мука"
    assert res[0].quantity == 150.0

def test_shopping_list_get_list_sort():
    recipe = Recipe("Панкейки", [Ingredient("Брусника", 100, "г"), Ingredient("Арбуз", 100, "г")])
    shopping = ShoppingList()
    shopping.add_recipe(recipe, 1)
    res = shopping.get_list()
    assert res[0].name == "Арбуз"
    assert res[1].name == "Брусника"

def test_shopping_list_add():
    pancakes = Recipe("Панкейки", [Ingredient("Мука", 100, "г")])
    cake = Recipe("Торт", [Ingredient("Сахар", 50, "г")])

    shopping1 = ShoppingList()
    shopping2 = ShoppingList()
    shopping1.add_recipe(pancakes, 1)
    shopping2.add_recipe(cake,1)

    combo_shopping = shopping1 + shopping2
    combo_res = combo_shopping.get_list()
    shop1_res = shopping1.get_list()
    shop2_res = shopping2.get_list()

    assert len(combo_res) == 2
    assert combo_res[0].name == "Мука"
    assert combo_res[0].quantity == 100.0
    assert combo_res[1].name == "Сахар"
    assert combo_res[1].quantity == 50.0

    assert len(shop1_res) == 1
    assert shop1_res[0].name == "Мука"
    assert shop1_res[0].quantity == 100.0

    assert len(shop2_res) == 1
    assert shop2_res[0].name == "Сахар"
    assert shop2_res[0].quantity == 50.0





