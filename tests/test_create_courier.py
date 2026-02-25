import pytest
import requests
import allure

from url import *
from data import *
from helpers import *


@allure.feature("Создание курьера")
class TestCourierCreation:

    @allure.title("Успешное создание курьера с уникальным логином")
    @allure.description("Проверяет, что курьер создаётся с уникальными login, password, firstName → статус 201.")
    def test_create_courier_success(self, created_courier):
        login, password, response = created_courier


        with allure.step("Проверяем ответ на запрос создания курьера"):
            assert response.status_code == EXPECTED_STATUS_CODES["created"], (ASSERT_MESSAGES["create_courier_success_status"].format(actual=response.status_code, response_text=response.text))
            assert response.json() == ERROR_MESSAGES["create_courier_success_response"], (ASSERT_MESSAGES["create_courier_success_json"])

        with allure.step(f"Проверяем, что курьер с login={login} существует и активен"):
            auth_response = requests.post(f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}", json={"login": login, "password": password})
            assert auth_response.status_code == EXPECTED_STATUS_CODES["success"], (ASSERT_MESSAGES["auth_courier_failure"].format(response_text=auth_response.text))
            assert "id" in auth_response.json(), ASSERT_MESSAGES["missing_id_in_auth"]

    @allure.title("Отсутствие поля login → ошибка 400")
    @allure.description("Проверяет, что при отсутствии login сервер возвращает 400 с сообщением об ошибке.")
    def test_create_courier_missing_login(self):
        with allure.step("Формируем запрос без поля login"):
            json_data = generate_unique_data(MISSING_LOGIN)

        with allure.step("Отправляем запрос на создание курьера"):
            response = requests.post(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}", json=json_data)

        with allure.step("Проверяем статус-код 400 и сообщение об ошибке"):
            assert response.status_code == EXPECTED_STATUS_CODES["bad_request"], (ASSERT_MESSAGES["create_courier_missing_field_status"].format(actual=response.status_code, response_text=response.text))
            expected_msg = ERROR_MESSAGES["create_courier_missing_login_message"]
            assert expected_msg in response.json().get("message", ""), (ASSERT_MESSAGES["incorrect_error_message"].format(response_json=response.json()))

    @allure.title("Отсутствие поля password → ошибка 400")
    @allure.description("Проверяет, что при отсутствии password сервер возвращает 400.")
    def test_create_courier_missing_password(self):
        with allure.step("Формируем запрос без поля password"):
            json_data = generate_unique_data(MISSING_PASSWORD)

        with allure.step("Отправляем запрос на создание курьера"):
            response = requests.post(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}", json=json_data)

        with allure.step("Проверяем статус-код 400 и сообщение об ошибке"):
            assert response.status_code == EXPECTED_STATUS_CODES["bad_request"], (ASSERT_MESSAGES["create_courier_missing_field_status"].format(actual=response.status_code, response_text=response.text))
            expected_msg = ERROR_MESSAGES["create_courier_missing_password_message"]
            assert expected_msg in response.json().get("message", ""), (ASSERT_MESSAGES["incorrect_error_message"].format(response_json=response.json()))

    @allure.title("Попытка создать курьера с уже существующим логином → 409")
    @allure.description("Проверяет, что повторный запрос с тем же логином вызывает ошибку 409.")
    def test_create_identical_couriers(self):
        data = generate_unique_data(VALID_COURIER)
        login = data["login"]
        password = data["password"]
        first_name = data["firstName"]

        with allure.step(f"Создаём первого курьера: login={login}"):
            response1 = create_courier(login, password, first_name)
            assert response1.status_code == EXPECTED_STATUS_CODES["created"], (f"Первый курьер не создан: {response1.text}")

        with allure.step(f"Повторяем запрос с тем же логином: {login} → ожидаем 409"):
            response2 = create_courier(login, password, first_name)

        with allure.step("Проверяем статус-код 409 и сообщение об ошибке"):
            assert response2.status_code == EXPECTED_STATUS_CODES["conflict"], (ASSERT_MESSAGES["create_identical_couriers_status"].format(actual=response2.status_code))
            expected_msg = ERROR_MESSAGES["create_identical_couriers_message"]
            actual_msg = response2.json().get("message", "")
            assert expected_msg in actual_msg, (ASSERT_MESSAGES["incorrect_conflict_message"].format(expected=expected_msg, actual=actual_msg))
