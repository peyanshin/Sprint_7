import requests
import allure

from url import *
from data import *
from api_methods.create_courier_method import *

@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.story("Проверка создания заказа с указанием цвета BLACK")
    def test_create_order_with_black_color(self):
        response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=ORDER_WITH_BLACK_COLOR)
        assert response.status_code == 201, (f"Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}")
        assert "track" in response.json(), "В ответе отсутствует поле track"

    @allure.story("Проверка создания заказа с указанием цвета GREY")
    def test_create_order_with_grey_color(self):
        response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=ORDER_WITH_GREY_COLOR)      
        assert response.status_code == 201, (f"Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}")
        assert "track" in response.json(), "В ответе отсутствует поле track"

    @allure.story("Проверка создания заказа с указанием обоих цветов (BLACK и GREY)")
    def test_create_order_with_both_colors(self):
        response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=ORDER_WITH_BOTH_COLORS)        
        assert response.status_code == 201, (f"Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}")
        assert "track" in response.json(), "В ответе отсутствует поле track"

    @allure.story("Проверка создания заказа без указания цвета")
    def test_create_order_without_color(self):
        response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}",json=ORDER_WITHOUT_COLOR)        
        assert response.status_code == 201, (f"Ожидался статус 201, получен {response.status_code}. Ответ: {response.text}")
        assert "track" in response.json(), "В ответе отсутствует поле track"

    @allure.story("Проверка получения списка заказов")
    def test_get_orders_list(self):
        response = requests.get(f"{BASE_URL}{ORDERS_LIST_ENDPOINT}")        
        assert response.status_code == 200, (f"Ожидался статус 200, получен {response.status_code}. Ответ: {response.text}")
        assert "orders" in response.json(), "В ответе отсутствует список заказов (поле orders)"
        assert isinstance(response.json()["orders"], list), "Поле orders не является списком"
