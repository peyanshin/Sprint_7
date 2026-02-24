import pytest
import allure
import requests

from url import *
from data import *
from helpers import *


@allure.feature("Создание курьера")
@pytest.mark.usefixtures("created_courier")
class TestCourierCreation:

    @allure.title("Успешное создание курьера с уникальным логином")
    @allure.description("Проверяет, что курьер создаётся с уникальными login, password, firstName → статус 201.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier_success(self, created_courier):
        login, password = created_courier

        with allure.step(f"Проверяем, что курьер с login={login} существует и активен"):
            auth_response = requests.post(
                f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
                json={"login": login, "password": password}
            )
            assert auth_response.status_code == 200, (f"Курьер не может авторизоваться: {auth_response.text}")
            assert "id" in auth_response.json(), ("В ответе отсутствует id курьера")

    @allure.title("Отсутствие поля login → ошибка 400")
    @allure.description("Проверяет, что при отсутствии login сервер возвращает 400 с сообщением об ошибке.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_courier_missing_login(self):
        with allure.step("Формируем запрос без поля login"):
            json_data = generate_unique_data(MISSING_LOGIN)

        with allure.step("Отправляем запрос на создание курьера"):
            response = requests.post(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}", json=json_data)

        with allure.step("Проверяем статус-код 400 и сообщение об ошибке"):
            assert response.status_code == 400, (f"Ожидался 400, получен {response.status_code}: {response.text}")
            assert "Недостаточно данных" in response.json().get("message", ""), (f"Неверное сообщение: {response.json()}")

    @allure.title("Отсутствие поля password → ошибка 400")
    @allure.description("Проверяет, что при отсутствии password сервер возвращает 400.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_courier_missing_password(self):
        with allure.step("Формируем запрос без поля password"):
            json_data = generate_unique_data(MISSING_PASSWORD)

        with allure.step("Отправляем запрос на создание курьера"):
            response = requests.post(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}", json=json_data)

        with allure.step("Проверяем статус-код 400 и сообщение об ошибке"):
            assert response.status_code == 400, (f"Ожидался 400, получен {response.status_code}: {response.text}")
            assert "Недостаточно данных" in response.json().get("message", ""), (f"Неверное сообщение: {response.json()}")

    @allure.title("Отсутствие поля firstName → успешное создание")
    @allure.description("Проверяет, что API допускает создание курьера без поля firstName. Ожидается статус 201.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_courier_missing_firstName(self):
        with allure.step("Формируем запрос без поля firstName"):
            json_data = generate_unique_data(MISSING_FIRSTNAME)

        with allure.step("Отправляем запрос на создание курьера"):
            response = requests.post(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}", json=json_data)

        with allure.step("Проверяем статус-код 201 и успешный ответ"):
            assert response.status_code == 201, (f"Ожидался 201 (API допускает отсутствие firstName), получен {response.status_code}: {response.text}")
            assert response.json() == {"ok": True}, (f"Неверный ответ: {response.json()}")

    @allure.title("Пустые значения полей → ошибка 400")
    @allure.description("Проверяет, что пустые значения полей вызывают ошибку 400.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_courier_empty_fields(self):
        with allure.step("Формируем запрос с пустыми значениями полей"):
            json_data = EMPTY_FIELDS

        with allure.step("Отправляем запрос на создание курьера"):
            response = requests.post(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}", json=json_data)

        with allure.step("Проверяем статус-код 400 и сообщение об ошибке"):
            assert response.status_code == 400, (f"Ожидался 400, получен {response.status_code}: {response.text}")
            assert "Недостаточно данных" in response.json().get("message", ""), (f"Неверное сообщение: {response.json()}")

    @allure.title("Проверка граничных значений для полей")
    @allure.description("Тестирует крайние случаи: очень длинные/короткие значения полей.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_courier_boundary_values(self):
        with allure.step("Формируем запрос с граничными значениями"):
            json_data = generate_unique_data(BOUNDARY_VALUES)
            json_data["login"] = generate_unique_login()

        with allure.step("Отправляем запрос на создание курьера"):
            response = requests.post(f"{BASE_URL}{CREATE_COURIER_ENDPOINT}", json=json_data)

        with allure.step("Проверяем ответ сервера"):
            assert response.status_code == 201, (f"Ожидался 201, получен {response.status_code}: {response.text}")
            assert "ok" in response.json(), (f"Неверный ответ: {response.json()}")

    @allure.title("Попытка создать курьера с уже существующим логином → 409")
    @allure.description("Проверяет, что повторный запрос с тем же логином вызывает ошибку 409.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_identical_couriers(self):
        data = generate_unique_data(VALID_COURIER)
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

        with allure.step("Проверяем статус-код 409 и сообщение об ошибке"):
            assert response2.status_code == 409, (f"Ожидался 409 (конфликт из‑за дублирующего логина), получен {response2.status_code}: {response2.text}")
            expected_message = ERROR_MESSAGES["duplicate_login"]
            assert expected_message in response2.json().get("message", ""), (
                f"Неверное сообщение об ошибке. Ожидалось: '{expected_message}', получено: {response2.json().get('message', 'отсутствует')}"
            )

        with allure.step("Проверяем, что в системе остался только один курьер с данным логином"):
            auth_response = requests.post(
                f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
                json={"login": login, "password": password}
            )
            assert auth_response.status_code == 200, (
                f"Курьер с login={login} не найден после проверки конфликта: {auth_response.text}"
            )
            assert "id" in auth_response.json(), (
                "В ответе авторизации отсутствует id курьера"
            )
            courier_id = auth_response.json()["id"]
            assert isinstance(courier_id, int) and courier_id > 0, (
                f"Некорректный id курьера: {courier_id}"
            )

        with allure.step("Дополнительно проверяем, что повторный запрос не создал дубликат"):
            response3 = create_courier(login, password, first_name)
            assert response3.status_code == 409, (
                f"Ожидался 409 при повторной попытке создания, получен {response3.status_code}: {response3.text}"
            )
            assert expected_message in response3.json().get("message", ""), (
                f"Сообщение об ошибке не соответствует ожидаемому при повторной проверке: {response3.json().get('message', 'отсутствует')}"
            )

        with allure.step("Проверяем, что количество курьеров с данным логином не увеличилось"):
            second_auth_response = requests.post(
                f"{BASE_URL}{LOGIN_COURIER_ENDPOINT}",
                json={"login": login, "password": password}
            )
            assert second_auth_response.status_code == 200, (
                f"Курьер стал недоступен после повторных проверок: {second_auth_response.text}"
            )
            assert second_auth_response.json().get("id") == courier_id, (
                "ID курьера изменился после повторных запросов — возможный признак дублирования"
            )
