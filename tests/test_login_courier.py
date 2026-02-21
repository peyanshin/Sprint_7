import requests
import time
import sys
import os

# Добавляем папки в sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

api_methods_path = os.path.join(project_root, "api_methods")
sys.path.insert(0, api_methods_path)

from url import BASE_URL, LOGIN_COURIER_ENDPOINT
from api_methods.create_courier_method import create_courier, delete_courier

import allure 

def login_courier(login: str, password: str) -> requests.Response:
    """Выполняет авторизацию курьера. Возвращает response."""
    return requests.post(
        f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
        json={
            "login": login,
            "password": password
        }
    )

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@allure.feature("Авторизация курьера")
class TestCourierLogin:

    @allure.story("Успешная авторизация")
    @allure.title("Проверка успешной авторизации курьера")
    @allure.description("Курьер создаётся, затем успешно авторизуется. Проверяется наличие id в ответе.")
    def test_successful_login(self):
        timestamp = int(time.time() * 1000)
        login = f"test_ninja_{timestamp}"
        password = "secure_pass_123"
        first_name = "TestSasuke"

        response = create_courier(login, password, first_name)
        assert response.status_code == 201, f"Не удалось создать курьера: {response.text}"

        login_response = login_courier(login, password)
        assert login_response.status_code == 200, f"Ожидался статус 200, получен {login_response.status_code}"
        assert "id" in login_response.json(), "В ответе отсутствует поле 'id'"
        assert isinstance(login_response.json()["id"], int), "Поле 'id' должно быть целым числом"


        delete_courier(login)

    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @allure.story("Ошибки авторизации")
    @allure.title("Проверка ошибки при пустом логине")
    @allure.description("Отправляется запрос с пустым полем login. Ожидаем статус 400 и сообщение об ошибке.")
    def test_missing_login(self):
        response = login_courier("", "1234")
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert response.json().get("message") == "Недостаточно данных для входа", \
            f"Неверное сообщение об ошибке: {response.json().get('message')}"


    #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @allure.story("Ошибки авторизации")
    @allure.title("Проверка ошибки при пустом пароле")
    @allure.description("Отправляется запрос с пустым полем password. Ожидаем статус 400 и сообщение об ошибке.")
    def test_missing_password(self):
        timestamp = int(time.time() * 1000)
        login = f"test_ninja_{timestamp}"
        password = "secure_pass_123"
        first_name = "TestSasuke"

        response = create_courier(login, password, first_name)
        assert response.status_code == 201, f"Не удалось создать курьера: {response.text}"

        response = login_courier(login, "")
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert response.json().get("message") == "Недостаточно данных для входа", \
            f"Неверное сообщение об ошибке: {response.json().get('message')}"


        delete_courier(login)

  #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @allure.story("Ошибки авторизации")
    @allure.title("Проверка ошибки при неверных credentials")
    @allure.description("Отправляется запрос с несуществующим логином/паролем. Ожидаем статус 404 и сообщение 'Учетная запись не найдена'.")
    def test_invalid_credentials(self):
        response = login_courier("nonexistent_login", "wrong_password")
        assert response.status_code == 404, f"Ожидался статус 404, получен {response.status_code}"
        assert response.json().get("message") == "Учетная запись не найдена", \
            f"Неверное сообщение об ошибке: {response.json().get('message')}"

   #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @allure.story("Ошибки валидации")
    @allure.title("Проверка отсутствия поля login в запросе")
    @allure.description("Отправляется JSON без поля login. Ожидаем статус 400 и сообщение о недостающих данных.")
    def test_no_login_field(self):
        response = requests.post(
            f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
            json={
                "password": "1234"
            }
        )
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert response.json().get("message") == "Недостаточно данных для входа", \
            f"Неверное сообщение об ошибке: {response.json().get('message')}"

    #----------------------------------------------------------------------------------------

    @allure.story("Ошибки валидации")
    @allure.title("Проверка отсутствия поля password в запросе")
    @allure.description("Отправляется JSON без поля password. Ожидаем статус 400 и сообщение о недостающих данных.")
    def test_no_password_field(self):
        timestamp = int(time.time() * 1000)
        login = f"test_ninja_{timestamp}"
        password = "secure_pass_123"
        first_name = "TestSasuke"

        response = create_courier(login, password, first_name)
        assert response.status_code == 201, f"Не удалось создать курьера: {response.text}"

        response = requests.post(
            f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
            json={  
                "login": login
            }
        )
        assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        assert response.json().get("message") == "Недостаточно данных для входа", \
            f"Неверное сообщение об ошибке: {response.json().get('message')}"


        delete_courier(login)
