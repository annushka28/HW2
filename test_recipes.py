import pytest

from main import Ingredient

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

