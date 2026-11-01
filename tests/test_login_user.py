import allure
import pytest
import requests

from tests.data import INCORRECT_CREDENTIALS, LOGIN_URL


class TestLoginUser:

    @allure.title("Логин под существующим пользователем")
    @allure.description(
        "Входим с email и паролем зарегистрированного пользователя. Проверяем: "
        "код ответа 200; success = true; в user вернулись email и name этого пользователя; "
        "accessToken начинается с 'Bearer '; refreshToken не пустой."
    )
    def test_login_existing_user_success(self, created_user):
        login_data = {"email": created_user["email"], "password": created_user["password"]}
        response = requests.post(LOGIN_URL, json=login_data)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"] == {"email": created_user["email"], "name": created_user["name"]}
        assert body["accessToken"].startswith("Bearer ")
        assert body["refreshToken"]

    @allure.title("Логин с неверным полем: {wrong_field}")
    @allure.description(
        "Входим с неверным email или неверным паролем существующего пользователя. "
        "Проверяем: код ответа 401; тело ответа — success = false и message "
        "'email or password are incorrect'."
    )
    @pytest.mark.parametrize("wrong_field", ["email", "password"])
    def test_login_with_wrong_credentials_error(self, created_user, wrong_field):
        login_data = {"email": created_user["email"], "password": created_user["password"]}
        login_data[wrong_field] = "wrong_" + login_data[wrong_field]
        response = requests.post(LOGIN_URL, json=login_data)

        assert response.status_code == 401
        assert response.json() == {"success": False, "message": INCORRECT_CREDENTIALS}
