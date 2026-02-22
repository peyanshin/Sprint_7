import pytest
import allure
import requests
import time
import random

from url import BASE_URL, CREATE_COURIER_ENDPOINT
from data import (
    VALID_COURIER,
    MISSING_LOGIN,
    MISSING_PASSWORD,
    MISSING_FIRSTNAME,
    EMPTY_FIELDS,
    BOUNDARY_VALUES,
    ERROR_MESSAGES,
    LOGIN_PREFIX,
    DEFAULT_PASSWORD
)
from api_methods.create_courier_method import create_courier, delete_courier, cleanup_test_couriers



def _generate_unique_data(template: dict) -> dict:
    """Генерирует уникальные данные с timestamp и случайным суффиксом."""
    timestamp = int(time.time() * 1000)
    random_suffix = str(random.randint(100000, 999999))  # 6 цифр


    return {
        key: (
            value.format(timestamp=timestamp, suffix=random_suffix)
            if isinstance(value, str) and ("{timestamp}" in value or "{suffix}" in value)
            else value
        )
        for key, value in template.items()
    }

def _generate_unique_login() -> str:
    """Генерирует гарантированно уникальный логин."""
    while True:
        timestamp = int(time.time() * 1000)
        random_suffix = str(random.randint(100000, 999999))
        login = f"{LOGIN_PREFIX}{timestamp}_{random_suffix}"
        if len(login) <= 50:
            return login

@pytest.fixture(scope="class")
def setup_cleanup():
    """Очищает тестовых курьеров перед запуском тестов."""
    cleanup_test_couriers(LOGIN_PREFIX)
    yield

@allure.feature("Создание курьера")
@pytest.mark.usefixtures("setup_cleanup")
class TestCourierCreation:

    @allure.title("Успешное создание курьера с уникальным логином")
    @allure.description("Проверяет, что курьер создаётся с уникальными login, password, firstName → статус 201.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier_success(self):
        with allure.step("Генерируем уникальные данные для курьера"):
            data = _generate_unique_data(VALID_COURIER)


        with allure.step(f"Отправляем запрос на создание курьера: login={data['login']}"):
            response = create_courier(data["login"], data["password"], data["firstName"])


        with allure.step("Проверяем статус-код 201 и ответ {'ok': True}"):
            assert response.status_code == 201, (
                f"Ожидался 201, получен {response.status_code}: {response.text}"
            )
            assert response.json() == {"ok": True}, (
                f"Неверный ответ: {response.json()}"
            )

    @allure.title("Отсутствие поля login → ошибка 400")
    @allure.description("Проверяет, что при отсутствии login сервер возвращает 400 с сообщением об ошибке.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_courier_missing_login(self):
        with allure.step("Формируем запрос без поля login"):
            json_data = _generate_unique_data(MISSING_LOGIN)


        with allure.step("Отправляем запрос и получаем ответ"):
            response = requests.post(
                f"{BASE_URL}{CREATE_COURIER_ENDPOINT}",
                json=json_data
            )
        with allure.step("Проверяем статус-код 400 и сообщение об ошибке"):
            assert response.status_code == 400, (
                f"Ожидался 400, получен {response.status_code}"
            )
            assert "Недостаточно данных" in response.json().get("message", ""), (
                f"Неверное сообщение: {response.json()}"
            )

    @allure.title("Отсутствие поля password → ошибка 400")
    @allure.description("Проверяет, что при отсутствии password сервер возвращает 400.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_courier_missing_password(self):
        with allure.step("Формируем запрос без поля password"):
            json_data = _generate_unique_data(MISSING_PASSWORD)

        with allure.step("Отправляем запрос и получаем ответ"):
            response = requests.post(
                f"{BASE_URL}{CREATE_COURIER_ENDPOINT}",
                json=json_data
            )

        with allure.step("Проверяем статус-код 400 и сообщение об ошибке"):
            assert response.status_code == 400, (
                f"Ожидался 400, получен {response.status_code}"
            )
            assert "Недостаточно данных" in response.json().get("message", ""), (
                f"Неверное сообщение: {response.json()}"
            )

    @allure.title("Отсутствие поля firstName → успешное создание")
    @allure.description(
        "Проверяет, что API допускает создание курьера без поля firstName. Ожидается статус 201."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_courier_missing_firstName(self):
        with allure.step("Формируем запрос без поля firstName"):
            json_data = _generate_unique_data(MISSING_FIRSTNAME)

        with allure.step("Отправляем запрос и получаем ответ"):
            response = requests.post(
                f"{BASE_URL}{CREATE_COURIER_ENDPOINT}",
                json=json_data
            )
        with allure.step("Проверяем статус-код 201 и успешный ответ"):
            assert response.status_code == 201, (
                f"Ожидался 201 (API допускает отсутствие firstName), получен {response.status_code}: {response.text}"
            )
            assert response.json() == {"ok": True}, (
                f"Неверный ответ: {response.json()}"
            )

    @allure.title("Пустые значения полей → ошибка 400")
    @allure.description("Проверяет, что пустые значения полей вызывают ошибку 400.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_courier_empty_fields(self):
        with allure.step("Формируем запрос с пустыми значениями полей"):
            json_data = EMPTY_FIELDS


        with allure.step("Отправляем запрос и получаем ответ"):
            response = requests.post(
                f"{BASE_URL}{CREATE_COURIER_ENDPOINT}",
                json=json_data
            )
        with allure.step("Проверяем статус-код 400 и сообщение об ошибке"):
            assert response.status_code == 400, (
                f"Ожидался 400, получен {response.status_code}"
            )
            assert "Недостаточно данных" in response.json().get("message", ""), (
                f"Неверное сообщение: {response.json()}"
            )

    @allure.title("Проверка граничных значений для полей")
    @allure.description("Тестирует крайние случаи: очень длинные/короткие значения полей.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_courier_boundary_values(self):
        with allure.step("Формируем запрос с граничными значениями"):
            json_data = _generate_unique_data(BOUNDARY_VALUES)
            json_data["login"] = _generate_unique_login()


        with allure.step("Отправляем запрос и получаем ответ"):
            response = requests.post(
                f"{BASE_URL}{CREATE_COURIER_ENDPOINT}",
                json=json_data
            )
        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 201, (
                f"Ожидался 201, получен {response.status_code}: {response.text}"
            )
            assert "ok" in response.json(), (
                f"Неверный ответ: {response.json()}"
            )

    @allure.title("Попытка создать курьера с уже существующим логином → 409")
    @allure.description("Проверяет, что повторный запрос с тем же логином вызывает ошибку 409.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_identical_couriers(self):
        data = _generate_unique_data(VALID_COURIER)
        login = data["login"]
        password = data["password"]
        first_name = data["firstName"]


        with allure.step(f"Создаём первого курьера: login={login}"):
            response1 = create_courier(login, password, first_name)
            assert response1.status_code == 201, (
                f"Первый курьер не создан: {response1.text}"
            )

        with allure.step(f"Повторяем запрос с тем же логином: {login} → ожидаем 409"):
            response2 = create_courier(login, password, first_name)

            assert response2.status_code == 409, (
                f"Ожидался 409, получен {response2.status_code}"
            )
            assert ERROR_MESSAGES["duplicate_login"] in response2.json().get("message", ""), (
                f"Неверное сообщение: {response2.json()}"
            )
