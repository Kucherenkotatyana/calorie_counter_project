import pytest


@pytest.fixture
def single_product_sample():
    single_product = [
        {
            "name": "fried potato",
            "calories": 307.3,
            "serving_size_g": 100,
            "fat_total_g": 14.7,
            "fat_saturated_g": 2.3,
            "protein_g": 3.4,
            "sodium_mg": 208,
            "potassium_mg": 126,
            "cholesterol_mg": 0,
            "carbohydrates_total_g": 41,
            "fiber_g": 3.8,
            "sugar_g": 0.3,
        },
    ]
    return single_product


@pytest.fixture
def multiple_products_sample():
    multiple_products = [
          {
            "name": "fried potato",
            "calories": 307.3,
            "serving_size_g": 100,
            "fat_total_g": 14.7,
            "fat_saturated_g": 2.3,
            "protein_g": 3.4,
            "sodium_mg": 208,
            "potassium_mg": 126,
            "cholesterol_mg": 0,
            "carbohydrates_total_g": 41,
            "fiber_g": 3.8,
            "sugar_g": 0.3
          },
          {
            "name": "onion",
            "calories": 44.7,
            "serving_size_g": 100,
            "fat_total_g": 0.2,
            "fat_saturated_g": 0,
            "protein_g": 1.4,
            "sodium_mg": 2,
            "potassium_mg": 35,
            "cholesterol_mg": 0,
            "carbohydrates_total_g": 10.1,
            "fiber_g": 1.4,
            "sugar_g": 4.7
          }
        ]
    return multiple_products
