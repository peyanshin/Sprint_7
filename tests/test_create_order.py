import requests
import allure
import os
import sys

# Добавляем папки в sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

api_methods_path = os.path.join(project_root, "api_methods")
sys.path.insert(0, api_methods_path)

from url import BASE_URL, CREATE_ORDER_ENDPOINT, ORDERS_LIST_ENDPOINT
from api_methods.create_courier_method import create_courier, delete_courier



@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.story("Проверка создания заказа с указанием цвета BLACK")
    def test_create_order_with_black_color(self):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": ["BLACK"]
        }

        response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=payload)
        
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}"
        assert "track" in response.json(), "В ответе отсутствует поле track"

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @allure.story("Проверка создания заказа с указанием цвета GREY")
    def test_create_order_with_grey_color(self):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": ["GREY"]
        }

        response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=payload)
        
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}"
        assert "track" in response.json(), "В ответе отсутствует поле track"

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @allure.story("Проверка создания заказа с указанием обоих цветов (BLACK и GREY)")
    def test_create_order_with_both_colors(self):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha",
            "color": ["BLACK", "GREY"]
        }

        response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=payload)
        
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}"
        assert "track" in response.json(), "В ответе отсутствует поле track"

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @allure.story("Проверка создания заказа без указания цвета")
    def test_create_order_without_color(self):
        payload = {
            "firstName": "Naruto",
            "lastName": "Uchiha",
            "address": "Konoha, 142 apt.",
            "metroStation": 4,
            "phone": "+7 800 355 35 35",
            "rentTime": 5,
            "deliveryDate": "2020-06-06",
            "comment": "Saske, come back to Konoha"
        }

        response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=payload)
        
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}"
        assert "track" in response.json(), "В ответе отсутствует поле track"

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @allure.story("Проверка получения списка заказов")
    def test_get_orders_list(self):
        response = requests.get(f"{BASE_URL}{ORDERS_LIST_ENDPOINT}")
        
        assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}"
        assert "orders" in response.json(), "В ответе отсутствует список заказов (поле orders)"
        assert isinstance(response.json()["orders"], list), "Поле orders не является списком"
