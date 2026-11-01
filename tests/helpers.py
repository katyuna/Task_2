import requests
from faker import Faker

from tests.data import INGREDIENTS_URL

fake = Faker()


def generate_user_data():
    return {
        "email": f"{fake.user_name()}{fake.random_number(digits=6)}@example.com",
        "password": fake.password(length=10),
        "name": fake.first_name(),
    }


def get_ingredient_ids():
    # Берём настоящие id ингредиентов из API, чтобы не зашивать их в код:
    # если список ингредиентов на сервере поменяется, тесты не сломаются.
    response = requests.get(INGREDIENTS_URL)
    return [ingredient["_id"] for ingredient in response.json()["data"]]
