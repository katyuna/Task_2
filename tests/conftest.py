import pytest
import requests

from tests.data import LOGIN_URL, REGISTER_URL, USER_URL
from tests.helpers import generate_user_data


@pytest.fixture
def created_user():
    user_data = generate_user_data()
    response = requests.post(REGISTER_URL, json=user_data)

    assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"

    access_token = response.json()["accessToken"]

    yield {**user_data, "access_token": access_token}

    requests.delete(USER_URL, headers={"Authorization": access_token})


@pytest.fixture
def new_user_data():
    user_data = generate_user_data()

    yield user_data

    response = requests.post(LOGIN_URL, json=user_data)
    if response.status_code == 200:
        access_token = response.json()["accessToken"]
        requests.delete(USER_URL, headers={"Authorization": access_token})
