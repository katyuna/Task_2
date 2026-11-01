"""Фикстуры pytest, общие для всех тестов.

conftest.py — специальный файл pytest. Фикстуры из него доступны во всех
тестах папки tests/ без импорта: достаточно указать имя фикстуры
в параметрах теста, например def test_login(created_user).
"""

import pytest
import requests

from tests.data import REGISTER_URL, USER_URL
from tests.helpers import generate_user_data


@pytest.fixture
def created_user():
    """Создаёт пользователя перед тестом и удаляет его после теста.

    Что получает тест — словарь:
        {
            "email": "...",          # почта пользователя
            "password": "...",       # пароль (нужен для теста логина)
            "name": "...",           # имя
            "access_token": "Bearer ...",  # токен для запросов с авторизацией
        }

    Как это работает:
    1. Код до yield выполняется ПЕРЕД тестом: регистрируем пользователя.
    2. yield отдаёт данные в тест, и тест выполняется.
    3. Код после yield выполняется ПОСЛЕ теста (даже если тест упал):
       удаляем пользователя, чтобы не оставлять мусор в сервисе.
    """
    # --- Подготовка: регистрируем нового пользователя через API ---
    user_data = generate_user_data()
    response = requests.post(REGISTER_URL, json=user_data)

    # Если пользователь не создался, тест запускать бессмысленно —
    # сразу сообщаем, что сломалась подготовка, а не сам тест.
    assert response.status_code == 200, f"Не удалось создать пользователя: {response.text}"

    # Токен понадобится и тесту, и для удаления пользователя.
    access_token = response.json()["accessToken"]

    # --- Передаём данные в тест ---
    yield {**user_data, "access_token": access_token}

    # --- Уборка: удаляем пользователя ---
    # Удаляем по токену, а не по email и паролю: тест мог их поменять
    # (например, тест изменения данных пользователя), а токен остаётся рабочим.
    requests.delete(USER_URL, headers={"Authorization": access_token})
