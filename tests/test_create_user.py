import allure
import pytest
import requests

from tests.data import REGISTER_URL, REQUIRED_FIELDS_MISSING, USER_ALREADY_EXISTS


class TestCreateUser:

    @allure.title("Создание нового пользователя")
    @allure.description(
        "Регистрируем пользователя с уникальными email, паролем и именем. Проверяем: "
        "код ответа 200; success = true; в user вернулись те же email и name; "
        "accessToken начинается с 'Bearer '; refreshToken не пустой."
    )
    def test_create_user_success(self, new_user_data):
        response = requests.post(REGISTER_URL, json=new_user_data)
        body = response.json()

        assert response.status_code == 200
        assert body["success"] is True
        assert body["user"] == {"email": new_user_data["email"], "name": new_user_data["name"]}
        assert body["accessToken"].startswith("Bearer ")
        assert body["refreshToken"]

    @allure.title("Создание пользователя, который уже зарегистрирован")
    @allure.description(
        "Повторно регистрируем пользователя с данными уже существующего. Проверяем: "
        "код ответа 403; тело ответа — success = false и message 'User already exists'."
    )
    def test_create_existing_user_error(self, created_user):

        user_data = {
            "email": created_user["email"],
            "password": created_user["password"],
            "name": created_user["name"],
        }
        response = requests.post(REGISTER_URL, json=user_data)

        assert response.status_code == 403
        assert response.json() == {"success": False, "message": USER_ALREADY_EXISTS}

    @allure.title("Создание пользователя без обязательного поля: {missing_field}")
    @allure.description(
        "Регистрируем пользователя без одного из обязательных полей (email, password или name). "
        "Проверяем: код ответа 403; тело ответа — success = false и message "
        "'Email, password and name are required fields'."
    )
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field_error(self, new_user_data, missing_field):

        user_data = {key: value for key, value in new_user_data.items() if key != missing_field}
        response = requests.post(REGISTER_URL, json=user_data)

        assert response.status_code == 403
        assert response.json() == {"success": False, "message": REQUIRED_FIELDS_MISSING}
