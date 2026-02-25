import pytest
import requests
import allure

from url import *
from data import *
from helpers import *


@allure.feature("Авторизация курьера")
class TestCourierLogin:

    @allure.title("Проверка успешной авторизации курьера")
    @allure.description("Курьер создаётся (проверяется статус 201), затем успешно авторизуется. Проверяется наличие и тип id в ответе.")
    def test_successful_login(self, created_courier):
        login, password, create_response = created_courier
        actual_create_status = create_response.status_code
        assert actual_create_status == EXPECTED_STATUS_CODES["created"], (ERROR_MESSAGES["created"].format(expected=EXPECTED_STATUS_CODES["created"], actual=actual_create_status))

        login_response = login_courier(login, password)
        actual_login_status = login_response.status_code
        assert actual_login_status == EXPECTED_STATUS_CODES["success"], (ERROR_MESSAGES["success"].format(expected=EXPECTED_STATUS_CODES["success"], actual=actual_login_status))

        response_json = login_response.json()
        assert "id" in response_json, ASSERT_MESSAGES["missing_id"]
        assert isinstance(response_json["id"], int), ASSERT_MESSAGES["invalid_id_type"]

    
    @allure.title("Проверка ошибок при отсутствии обязательных полей")
    @allure.description("Проверяются ожидаемый статус 400 и сообщение 'Недостаточно данных для входа' для сценариев: 1. пустой login/password 2. отсутствие полей login/password.")
    @pytest.mark.parametrize(
        "test_case, payload",
        [
            ("Пустой login", {"login": "", "password": "1234"}),
            ("Пустой password", {"login": "valid_login", "password": ""}),
            ("Нет поля login", {"password": "1234"}),
            ("Нет поля password", {"login": "valid_login"}),
        ],
        ids=[
            "empty_login",
            "empty_password",
            "missing_login_field",
            "missing_password_field"
        ]
    )
    def test_missing_or_empty_fields(self, test_case, payload):
        with allure.step(f"Сценарий: {test_case}"):
            response = requests.post(f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}", json=payload)

            actual_status = response.status_code
            assert actual_status == EXPECTED_STATUS_CODES["bad_request"], (ERROR_MESSAGES["bad_request"].format(expected=EXPECTED_STATUS_CODES["bad_request"],actual=actual_status))

            actual_message = response.json().get("message")
            expected_message = ERROR_MESSAGES["missing_fields"]
            assert actual_message == expected_message, (ERROR_MESSAGES["unexpected_error_message"].format(actual_message=actual_message))

    @allure.title("Проверка ошибки при неверных credentials")
    @allure.description("Проверяется ожидаемый статус 404 и сообщение 'Учетная запись не найдена'при отправке запроса с несуществующим логином/паролем.")
    def test_invalid_credentials(self):
        response = login_courier("nonexistent_login", "wrong_password")

        actual_status = response.status_code
        assert actual_status == EXPECTED_STATUS_CODES["not_found"], (ERROR_MESSAGES["not_found"].format(expected=EXPECTED_STATUS_CODES["not_found"], actual=actual_status))

        actual_message = response.json().get("message")
        expected_message = ERROR_MESSAGES["account_not_found"]
        assert actual_message == expected_message, (ERROR_MESSAGES["unexpected_error_message"].format(actual_message=actual_message))
