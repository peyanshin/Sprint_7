import requests

from url import *


def create_courier(login: str, password: str, first_name: str) -> requests.Response:
    """Создание курьера"""
    response = requests.post(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}", json={"login": login,"password": password,"firstName": first_name})
    return response

def delete_courier(login: str, password: str) -> bool:
    """Удаление курьера"""
    auth_response = requests.post(f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}", json={"login": login, "password": password})
    if auth_response.status_code != 200:
        return False

    courier_id = auth_response.json().get("id")
    if not courier_id:
        return False

    delete_response = requests.delete(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}/{courier_id}")
    return delete_response.status_code == 200

def cleanup_test_couriers(prefix: str):
    """Удаляет всех курьеров с логинами, начинающимися на prefix."""
    response = requests.get(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}")
    if response.status_code == 200:
        for courier in response.json():
            if courier.get("login", "").startswith(prefix):
                delete_courier(courier["login"], "1234")
