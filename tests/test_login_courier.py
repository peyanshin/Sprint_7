import requests
import allure

from url import *
from conftest import *
from data import *



def login_courier(login: str, password: str) -> requests.Response:
    """Выполняет авторизацию курьера. Возвращает response."""
    return requests.post(
        f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
        json={"login": login, "password": password}
    )



@allure.feature("Авторизация курьера")
class TestCourierLogin:

    @allure.story("Успешная авторизация")
    @allure.title("Проверка успешной авторизации курьера")
    @allure.description("Курьер создаётся, затем успешно авторизуется. Проверяется наличие id в ответе.")
    def test_successful_login(self, created_courier):
        login, password = created_courier
        login_response = login_courier(login, password)
        
        expected_status = EXPECTED_STATUS_CODES["success"]
        actual_status = login_response.status_code
        assert actual_status == expected_status, STATUS_ERROR_MESSAGES["success"].format(
            expected=expected_status,
            actual=actual_status
        )
        
        assert "id" in login_response.json(), ASSERT_MESSAGES["missing_id"]
        assert isinstance(login_response.json()["id"], int), ASSERT_MESSAGES["invalid_id_type"]

    @allure.story("Ошибки авторизации")
    @allure.title("Проверка ошибки при пустом логине")
    @allure.description("Отправляется запрос с пустым полем login. Ожидаем статус 400 и сообщение об ошибке.")
    def test_missing_login(self):
        response = login_courier("", "1234")
        
        expected_status = EXPECTED_STATUS_CODES["bad_request"]
        actual_status = response.status_code
        assert actual_status == expected_status, STATUS_ERROR_MESSAGES["bad_request"].format(
            expected=expected_status,
            actual=actual_status
        )
        
        expected_message = AUTH_ERROR_MESSAGES["missing_fields"]
        actual_message = response.json().get("message")
        assert actual_message == expected_message, f"Неверное сообщение об ошибке: {actual_message}"

    @allure.story("Ошибки авторизации")
    @allure.title("Проверка ошибки при пустом пароле")
    @allure.description("Отправляется запрос с пустым полем password. Ожидаем статус 400 и сообщение об ошибке.")
    def test_missing_password(self, created_courier):
        login, _ = created_courier
        response = login_courier(login, "")
        
        expected_status = EXPECTED_STATUS_CODES["bad_request"]
        actual_status = response.status_code
        assert actual_status == expected_status, STATUS_ERROR_MESSAGES["bad_request"].format(
            expected=expected_status,
            actual=actual_status
        )
        
        expected_message = AUTH_ERROR_MESSAGES["missing_fields"]
        actual_message = response.json().get("message")
        assert actual_message == expected_message, f"Неверное сообщение об ошибке: {actual_message}"

    @allure.story("Ошибки авторизации")
    @allure.title("Проверка ошибки при неверных credentials")
    @allure.description("Отправляется запрос с несуществующим логином/паролем. Ожидаем статус 404 и сообщение 'Учетная запись не найдена'.")
    def test_invalid_credentials(self):
        response = login_courier("nonexistent_login", "wrong_password")
        
        expected_status = EXPECTED_STATUS_CODES["not_found"]
        actual_status = response.status_code
        assert actual_status == expected_status, STATUS_ERROR_MESSAGES["not_found"].format(
            expected=expected_status,
            actual=actual_status
        )
        
        expected_message = AUTH_ERROR_MESSAGES["account_not_found"]
        actual_message = response.json().get("message")
        assert actual_message == expected_message, f"Неверное сообщение об ошибке: {actual_message}"

    @allure.story("Ошибки валидации")
    @allure.title("Проверка отсутствия поля login в запросе")
    @allure.description("Отправляется JSON без поля login. Ожидаем статус 400 и сообщение о недостающих данных.")
    def test_no_login_field(self):
        response = requests.post(
            f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
            json={"password": "1234"}
        )

        expected_status = EXPECTED_STATUS_CODES["bad_request"]
        actual_status = response.status_code
        assert actual_status == expected_status, STATUS_ERROR_MESSAGES["bad_request"].format(
            expected=expected_status,
            actual=actual_status
        )

        expected_message = AUTH_ERROR_MESSAGES["missing_fields"]
        actual_message = response.json().get("message")
        assert actual_message == expected_message, f"Неверное сообщение об ошибке: {actual_message}"

    @allure.story("Ошибки валидации")
    @allure.title("Проверка отсутствия поля password в запросе")
    @allure.description("Отправляется JSON без поля password. Ожидаем статус 400 и сообщение о недостающих данных.")
    def test_no_password_field(self, created_courier):
        login, _ = created_courier
        response = requests.post(
            f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
            json={"login": login}
        )

        expected_status = EXPECTED_STATUS_CODES["bad_request"]
        actual_status = response.status_code
        assert actual_status == expected_status, STATUS_ERROR_MESSAGES["bad_request"].format(
            expected=expected_status,
            actual=actual_status
        )

        expected_message = AUTH_ERROR_MESSAGES["missing_fields"]
        actual_message = response.json().get("message")
        assert actual_message == expected_message, f"Неверное сообщение об ошибке: {actual_message}"
