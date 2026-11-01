import allure
import requests

from tests.data import INTERNAL_SERVER_ERROR, NO_INGREDIENTS, ORDERS_URL
from tests.helpers import get_ingredient_ids


class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    @allure.description(
        "Создаём заказ из двух ингредиентов, передав токен пользователя. Проверяем: "
        "код ответа 200; success = true; owner.email заказа совпадает с email пользователя; "
        "id ингредиентов в заказе совпадают с переданными."
    )
    def test_create_order_with_auth_success(self, created_user):
        ingredient_ids = get_ingredient_ids()[:2]
        response = requests.post(
            ORDERS_URL,
            headers={"Authorization": created_user["access_token"]},
            json={"ingredients": ingredient_ids},
        )
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["order"]["owner"]["email"] == created_user["email"]
        assert [ingredient["_id"] for ingredient in body["order"]["ingredients"]] == ingredient_ids

    @allure.title("Создание заказа без авторизации с ингредиентами")
    @allure.description(
        "Создаём заказ из двух ингредиентов без токена. Проверяем: "
        "код ответа 200; success = true; в order есть номер заказа (целое число)."
    )
    def test_create_order_without_auth_success(self):
        ingredient_ids = get_ingredient_ids()[:2]
        response = requests.post(ORDERS_URL, json={"ingredients": ingredient_ids})
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert isinstance(body["order"]["number"], int)

    @allure.title("Создание заказа без ингредиентов")
    @allure.description(
        "Создаём заказ с пустым списком ингредиентов. Проверяем: код ответа 400; "
        "тело ответа — success = false и message 'Ingredient ids must be provided'."
    )
    def test_create_order_without_ingredients_error(self, created_user):
        response = requests.post(
            ORDERS_URL,
            headers={"Authorization": created_user["access_token"]},
            json={"ingredients": []},
        )

        assert response.status_code == 400
        assert response.json() == {"success": False, "message": NO_INGREDIENTS}

    @allure.title("Создание заказа с неверным хешем ингредиента")
    @allure.description(
        "Создаём заказ с ингредиентом, у которого неверный хеш ('invalid'). Проверяем: "
        "код ответа 500; в теле ответа (HTML-страница) есть текст 'Internal Server Error'."
    )
    def test_create_order_with_invalid_ingredient_hash_error(self, created_user):
        response = requests.post(
            ORDERS_URL,
            headers={"Authorization": created_user["access_token"]},
            json={"ingredients": ["invalid"]},
        )

        assert response.status_code == 500
        assert INTERNAL_SERVER_ERROR in response.text
