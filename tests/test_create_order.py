import requests
import allure

from data import *
from url import  *


@allure.feature("Создание заказа")
class TestCreateOrder:

    def _assert_order_created(self, response):
        """Общая проверка для успешного создания заказа."""
        expected = EXPECTED_STATUS_CODES["created"]
        assert response.status_code == expected, STATUS_ERROR_MESSAGES["create_order"].format(
            expected=expected,
            actual=response.status_code,
            response_text=response.text
        )
        assert "track" in response.json(), ASSERT_MESSAGES["missing_track"]

    def _assert_orders_list(self, response):
        """Общая проверка для списка заказов."""
        expected = EXPECTED_STATUS_CODES["success"]
        assert response.status_code == expected, STATUS_ERROR_MESSAGES["get_orders"].format(
            expected=expected,
            actual=response.status_code,
            response_text=response.text
        )
        assert "orders" in response.json(), ASSERT_MESSAGES["missing_orders"]
        assert isinstance(response.json()["orders"], list), ASSERT_MESSAGES["invalid_orders_type"]

    @allure.story("Проверка создания заказа с указанием цвета BLACK")
    def test_create_order_with_black_color(self):
        response = requests.post(
            f"{BASE_URL}{CREATE_ORDER_ENDPOINT}",
            json=ORDER_PAYLOADS["black"]
        )
        self._assert_order_created(response)

    @allure.story("Проверка создания заказа с указанием цвета GREY")
    def test_create_order_with_grey_color(self):
        response = requests.post(
            f"{BASE_URL}{CREATE_ORDER_ENDPOINT}",
            json=ORDER_PAYLOADS["grey"]
        )
        self._assert_order_created(response)

    @allure.story("Проверка создания заказа с указанием обоих цветов (BLACK и GREY)")
    def test_create_order_with_both_colors(self):
        response = requests.post(
            f"{BASE_URL}{CREATE_ORDER_ENDPOINT}",
            json=ORDER_PAYLOADS["both"]
        )
        self._assert_order_created(response)

    @allure.story("Проверка создания заказа без указания цвета")
    def test_create_order_without_color(self):
        response = requests.post(
            f"{BASE_URL}{CREATE_ORDER_ENDPOINT}",
            json=ORDER_PAYLOADS["no_color"]
        )
        self._assert_order_created(response)

    @allure.story("Проверка получения списка заказов")
    def test_get_orders_list(self):
        response = requests.get(f"{BASE_URL}{ORDERS_LIST_ENDPOINT}")
        self._assert_orders_list(response)
