import pytest
import requests
import time
import sys
import os

# Добавляем корневую папку проекта в путь поиска модулей
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from url import BASE_URL, CREATE_COURIER_ENDPOINT, LOGIN_COURIER_ENDPOINT

def create_courier(login: str, password: str, first_name: str) -> requests.Response:
    """Создаёт курьера. Возвращает response."""
    response = requests.post(
        f"{BASE_URL}{CREATE_COURIER_ENDPOINT}",
        json={
            "login": login,
            "password": password,
            "firstName": first_name
        }
    )
    return response

def delete_courier(login: str) -> bool:
    """
    Удаляет курьера по логину (если API поддерживает).
    Возвращает True, если удаление прошло успешно.
    """
    # Получаем id курьера через логин
    response = requests.post(
        f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
        json={"login": login, "password": "secure_pass_123"}  # Пароль из фикстуры
    )
    if response.status_code != 200:
        return False

    courier_id = response.json().get("id")
    if not courier_id:
        return False

    # Удаляем курьера
    delete_response = requests.delete(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}/{courier_id}")
    return delete_response.status_code == 200

@pytest.fixture(scope="function")
def unique_courier():
    """
    Фикстура: создаёт курьера с уникальным логином (на основе timestamp).
    Удаляет курьера после теста (если поддерживается).
    """
    timestamp = int(time.time() * 1000)
    login = f"test_ninja_{timestamp}"
    password = "secure_pass_123"
    first_name = "TestSasuke"

    response = create_courier(login, password, first_name)
    assert response.status_code == 201, f"Не удалось создать курьера: {response.text}"

    yield login  # Возвращаем логин для тестов

    # Попытка удалить курьера после теста
    delete_courier(login)
