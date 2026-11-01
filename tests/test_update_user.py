import allure
import pytest
import requests

from tests.data import UNAUTHORISED, USER_URL
from tests.helpers import generate_user_data


class TestUpdateUser:

    @allure.title("Изменение поля {field} с авторизацией")
    @allure.description(
        "Меняем одно поле пользователя (email, password или name), передав его токен. "
        "Проверяем: код ответа 200; тело ответа — success = true и user с актуальными "
        "email и name (при смене пароля email и name не меняются)."
    )
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_update_user_with_auth_success(self, created_user, field):

        new_value = generate_user_data()[field]
        response = requests.patch(
            USER_URL,
            headers={"Authorization": created_user["access_token"]},
            json={field: new_value},
        )

        expected_user = {"email": created_user["email"], "name": created_user["name"]}
        if field in expected_user:
            expected_user[field] = new_value

        assert response.status_code == 200
        assert response.json() == {"success": True, "user": expected_user}

    @allure.title("Изменение поля {field} без авторизации")
    @allure.description(
        "Пытаемся изменить поле пользователя (email, password или name) без токена. "
        "Проверяем: код ответа 401; тело ответа — success = false и message "
        "'You should be authorised'."
    )
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_update_user_without_auth_error(self, field):
        
        new_value = generate_user_data()[field]
        response = requests.patch(USER_URL, json={field: new_value})

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": UNAUTHORISED}
