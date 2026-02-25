import pytest
import requests
import allure

from url import *
from data import *


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Проверка успешного создания заказа")
    @allure.description(
        "Проверяет, что заказ успешно создан: "
        "1. Статус ответа — 201 Created; "
        "2. В теле ответа присутствует поле 'track'."
    )
    def _assert_order_created(self, response):
        expected = EXPECTED_STATUS_CODES["created"]
        assert response.status_code == expected, ERROR_MESSAGES["create_order"].format(expected=expected, actual=response.status_code, response_text=response.text)
        assert "track" in response.json(), ASSERT_MESSAGES["missing_track"]

    @allure.title("Проверка получения списка заказов")
    @allure.description(
        "Проверяет корректность получения списка заказов: "
        "1. Статус ответа — 200 OK; "
        "2. В ответе присутствует поле 'orders'; "
        "3. Поле 'orders' имеет тип списка (list)."
    )
    def _assert_orders_list(self, response):
        expected = EXPECTED_STATUS_CODES["success"]
        assert response.status_code == expected, ERROR_MESSAGES["get_orders"].format(expected=expected, actual=response.status_code, response_text=response.text)

        json_response = response.json()
        assert "orders" in json_response, ASSERT_MESSAGES["missing_orders"]
        assert isinstance(json_response["orders"], list), ASSERT_MESSAGES["invalid_orders_type"]

    @allure.title("Проверка создания заказа с разными вариантами цвета")
    @allure.description(
        "Тестирует создание заказа с различными вариантами указания цвета: "
        "1. Только BLACK; "
        "2. Только GREY; "
        "3. Оба цвета (BLACK и GREY); "
        "4. Без указания цвета. "
        "Для каждого варианта проверяется успешный статус создания заказа и наличие track-номера."
    )
    @pytest.mark.parametrize("color_key,payload", [
        ("BLACK", ORDER_PAYLOADS["black"]),
        ("GREY", ORDER_PAYLOADS["grey"]),
        ("BOTH", ORDER_PAYLOADS["both"]),
        ("NO_COLOR", ORDER_PAYLOADS["no_color"]),
    ])
    def test_create_order_with_colors(self, color_key, payload):
        response = requests.post(f"{BASE_URL}{CREATE_ORDER_ENDPOINT}", json=payload)
        self._assert_order_created(response)

    @allure.title("Проверка получения списка заказов")
    @allure.description(
        "Проверяет корректность получения списка заказов: "
        "1. Статус ответа — 200 OK; "
        "2. В ответе присутствует поле 'orders'; "
        "3. Поле 'orders' имеет тип списка (list)."
    )
    def test_get_orders_list(self):
        response = requests.get(f"{BASE_URL}{ORDERS_LIST_ENDPOINT}")
        self._assert_orders_list(response)
