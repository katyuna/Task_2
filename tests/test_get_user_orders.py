import allure
import requests

from tests.data import ORDERS_URL, UNAUTHORISED
from tests.helpers import get_ingredient_ids


class TestGetUserOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    @allure.description(
        "Создаём пользователю заказ и запрашиваем его заказы с токеном. Проверяем: "
        "код ответа 200; success = true; в списке orders ровно один заказ, и его номер "
        "совпадает с номером созданного заказа; total и totalToday — целые числа."
    )
    def test_get_orders_with_auth_success(self, created_user):
        headers = {"Authorization": created_user["access_token"]}
        # Подготовка: у нового пользователя заказов нет, поэтому создаём один.
        order_response = requests.post(
            ORDERS_URL,
            headers=headers,
            json={"ingredients": get_ingredient_ids()[:2]},
        )
        order_number = order_response.json()["order"]["number"]

        response = requests.get(ORDERS_URL, headers=headers)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert [order["number"] for order in body["orders"]] == [order_number]
        assert isinstance(body["total"], int)
        assert isinstance(body["totalToday"], int)

    @allure.title("Получение заказов неавторизованного пользователя")
    @allure.description(
        "Запрашиваем заказы пользователя без токена. Проверяем: код ответа 401; "
        "тело ответа — success = false и message 'You should be authorised'."
    )
    def test_get_orders_without_auth_error(self):
        response = requests.get(ORDERS_URL)

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": UNAUTHORISED}
