import time
import random
import requests

from url import BASE_URL, CREATE_COURIER_ENDPOINT, LOGIN_COURIER_ENDPOINT


def login_courier(login: str, password: str) -> requests.Response:
    """Авторизация курьера"""
    return requests.post(
        f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
        json={"login": login, "password": password}
    )

def create_courier(login: str, password: str, first_name: str) -> requests.Response:
    """Создание курьера"""
    json_data = {"login": login, "password": password, "firstName": first_name}
    return requests.post(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}", json=json_data)


def delete_courier(login: str, password: str) -> requests.Response:
    """Удаление курьера через получение ID и DELETE-запрос"""
    auth_response = login_courier(login, password)
    if auth_response.status_code != 200:
        return auth_response

    courier_id = auth_response.json().get("id")
    if not courier_id:
        return auth_response

    return requests.delete(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}/{courier_id}")

def generate_unique_data(template: dict) -> dict:
    """Генерирует уникальные данные с timestamp и случайным суффиксом."""
    timestamp = int(time.time() * 1000)
    random_suffix = str(random.randint(100000, 999999))

    return {
        key: (
            value.format(timestamp=timestamp, suffix=random_suffix)
            if isinstance(value, str) and ("{timestamp}" in value or "{suffix}" in value)
            else value
        )
        for key, value in template.items()
    }

def generate_unique_login() -> str:
    """Генерирует гарантированно уникальный логин."""
    while True:
        timestamp = int(time.time() * 1000)
        random_suffix = str(random.randint(100000, 999999))
        login = f"test_ninja_{timestamp}_{random_suffix}"
        if len(login) <= 50:
            return login

def is_courier_active(login: str, password: str) -> bool:
    """Проверяет, что курьер существует и активен."""
    auth_response = requests.post(
        f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
        json={"login": login, "password": password}
    )
    return auth_response.status_code == 200 and "id" in auth_response.json()
