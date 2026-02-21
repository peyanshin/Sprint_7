import sys
import os
import requests
import time
import allure  # Импорт Allure

# Добавляем папки в sys.path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

api_methods_path = os.path.join(project_root, "api_methods")
sys.path.insert(0, api_methods_path)

# Импорты
from url import BASE_URL, CREATE_COURIER_ENDPOINT
from api_methods.create_courier_method import unique_courier, create_courier

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@allure.feature("Создание курьера")
class TestCourierCreation:

    @allure.title("Успешное создание курьера с уникальным логином")
    @allure.description("Проверяет, что курьер создаётся с уникальными login, password, firstName → статус 201.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier_success(self):
        with allure.step("Генерируем уникальные данные для курьера"):
            timestamp = int(time.time() * 1000)
            login = f"test_ninja_{timestamp}"
            password = "secure_pass_123"
            first_name = "TestSasuke"

        with allure.step(f"Отправляем запрос на создание курьера: login={login}"):
            print(f"Отправляется запрос на создание курьера: login={login}, firstName={first_name}")
            response = create_courier(login, password, first_name)
            print(f"Статус-код: {response.status_code}, ответ: {response.json()}")


        with allure.step("Проверяем статус-код 201 и ответ {'ok': True}"):
            assert response.status_code == 201, (
                f"Ожидался 201, получен {response.status_code}: {response.text}"
            )
            assert response.json() == {"ok": True}, (
                f"Неверный ответ: {response.json()}"
            )

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @allure.title("Отсутствие поля login → ошибка 400")
    @allure.description("Проверяет, что при отсутствии login сервер возвращает 400 с сообщением об ошибке.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_courier_missing_login(self):
        with allure.step("Формируем запрос без поля login"):
            json_data = {
                "password": "1234",
                "firstName": "saske"
            }
            print(f"Отправляется запрос без login: {json_data}")

        with allure.step("Отправляем запрос и получаем ответ"):
            response = requests.post(
                f"{BASE_URL}{CREATE_COURIER_ENDPOINT}",
                json=json_data
            )
            print(f"[missing_login] Статус-код: {response.status_code}, ответ: {response.json()}")


        with allure.step("Проверяем статус-код 400 и сообщение об ошибке"):
            assert response.status_code == 400, (
                f"Ожидался 400, получен {response.status_code}"
            )
            assert "Недостаточно данных" in response.json().get("message", ""), (
                f"Неверное сообщение: {response.json()}"
            )

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @allure.title("Отсутствие поля password → ошибка 400")
    @allure.description("Проверяет, что при отсутствии password сервер возвращает 400.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_courier_missing_password(self):
        timestamp = int(time.time() * 1000)
        with allure.step("Формируем запрос без поля password"):
            json_data = {
                "login": f"ninja_{timestamp}",
                "firstName": "saske"
            }
            print(f"Отправляется запрос без password: {json_data}")


        with allure.step("Отправляем запрос и получаем ответ"):
            response = requests.post(
                f"{BASE_URL}{CREATE_COURIER_ENDPOINT}",
                json=json_data
            )
            print(f"[missing_password] Статус-код: {response.status_code}, ответ: {response.json()}")


        with allure.step("Проверяем статус-код 400 и сообщение об ошибке"):
            assert response.status_code == 400, (
                f"Ожидался 400, получен {response.status_code}"
            )
            assert "Недостаточно данных" in response.json().get("message", ""), (
                f"Неверное сообщение: {response.json()}"
            )

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @allure.title("Отсутствие поля firstName → проверка поведения API")
    @allure.description(
        "Проверяет, как API обрабатывает отсутствие firstName. "
        "Если API допускает отсутствие — ожидается 201. Если требует — 400."
    )
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_courier_missing_firstName(self):
        timestamp = int(time.time() * 1000)
        json_data = {
            "login": f"ninja_{timestamp}",
            "password": "1234"
        }

        with allure.step("Отправляем запрос без firstName"):
            print(f"Отправляется запрос без firstName: {json_data}")
            response = requests.post(
                f"{BASE_URL}{CREATE_COURIER_ENDPOINT}",
                json=json_data
            )
            print(f"Статус-код: {response.status_code}, ответ: {response.json()}")  # Исправлено: f"..."


        with allure.step("Проверяем ответ сервера"):
            # Вариант 1: API допускает отсутствие firstName
            assert response.status_code == 201, (
                f"Ожидался 201 (API допускает отсутствие firstName), получен {response.status_code}: {response.text}"
            )
            assert "ok" in response.json(), (
                f"Неверный ответ: {response.json()}"
            )
            
            # Вариант 2: API требует firstName
            # assert response.status_code == 400, (
            #     f"Ожидался 400 (firstName обязателен), получен {response.status_code}"
            # )
            # assert "Недостаточно данных" in response.json().get("message", ""), (
            #     f"Неверное сообщение: {response.json()}"
            # )

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @allure.title("Попытка создать курьера с существующим логином → 409")
    @allure.description("Проверяет, что дублирующий логин вызывает ошибку 409.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier_duplicate_login(self, unique_courier):
        with allure.step(f"Используем существующий логин: {unique_courier}"):
            response = create_courier(unique_courier, "another_pass", "DuplicateSasuke")
            print(f"[duplicate_login] Статус-код: {response.status_code}, ответ: {response.json()}")

        with allure.step("Проверяем статус-код 409 и сообщение"):
            assert response.status_code == 409, (
                f"Ожидался 409, получен {response.status_code}"
            )
            assert "Этот логин уже используется" in response.json().get("message", ""), (
                f"Неверное сообщение: {response.json()}"
            )

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @allure.title("Пустые поля → ошибка 400")
    @allure.description("Проверяет, что пустые значения полей вызывают ошибку 400.")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_courier_empty_fields(self):
        json_data = {
            "login": "",
            "password": "",
            "firstName": ""
        }

        with allure.step("Формируем запрос с пустыми значениями всех полей"):
            print(f"Отправляется запрос с пустыми полями: {json_data}")

        with allure.step("Отправляем запрос и получаем ответ"):
            response = requests.post(
                f"{BASE_URL}{CREATE_COURIER_ENDPOINT}",
                json=json_data
            )
            print(f"[empty_fields] Статус-код: {response.status_code}, ответ: {response.json()}")

        with allure.step("Проверяем статус-код 400 и сообщение об ошибке"):
            assert response.status_code == 400, (
                f"Ожидался 400, получен {response.status_code}"
            )
            assert "Недостаточно данных" in response.json().get("message", ""), (
                f"Неверное сообщение: {response.json()}"
            )

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @allure.title("Попытка создать идентичных курьеров → 409")
    @allure.description("Проверяет, что повторный запрос с теми же данными вызывает ошибку 409.")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_identical_couriers(self):
        timestamp = int(time.time() * 1000)
        login = f"clone_ninja_{timestamp}"
        password = "clone_pass_789"
        first_name = "CloneSasuke"

        with allure.step(f"Создаём первого курьера: login={login}"):
            response1 = create_courier(login, password, first_name)
            print(f"[identical_1] Статус-код: {response1.status_code}, ответ: {response1.json()}")
            assert response1.status_code == 201, (
                f"Первый курьер не создан: {response1.text}"
            )

        with allure.step(f"Повторяем запрос с тем же логином: {login} → ожидаем 409"):
            response2 = create_courier(login, password, first_name)
            print(f"[identical_2] Статус-код: {response2.status_code}, ответ: {response2.json()}")

            assert response2.status_code == 409, (
                f"Ожидался 409, получен {response2.status_code}"
            )
            assert "Этот логин уже используется" in response2.json().get("message", ""), (
                f"Неверное сообщение: {response2.json()}"
            )

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @allure.title("Проверка граничных значений для полей")
    @allure.description("Тестирует крайние случаи: очень длинные/короткие значения полей.")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_courier_boundary_values(self):
        timestamp = int(time.time() * 1000)
        # Генерируем уникальный логин с длинной последовательностью 'a'
        long_login = f"boundary_test_{timestamp}_{'a' * 200}"
        short_password = "a!  # если API допускает 1 символ"
        long_name = "X! * 100"


        json_data = {
            "login": long_login,
            "password": short_password,
            "firstName": long_name  
        }

        with allure.step(f"Отправляем запрос с граничными значениями: {json_data}"):
            print(f"Отправляется запрос с граничными значениями: {json_data}")
            response = requests.post(
                f"{BASE_URL}{CREATE_COURIER_ENDPOINT}",
                json=json_data
            )
            print(f"[boundary_values] Статус-код: {response.status_code}, ответ: {response.json()}")


        with allure.step("Проверяем ответ сервера"):
            # Если API должен принимать граничные значения
            expected_status = 201
            assert response.status_code == expected_status, (
                f"Ожидался {expected_status}, получен {response.status_code}: {response.text}"
            )

            # Если API должен отклонять (например, из-за длины)
            # expected_status = 400
            # assert response.status_code == expected_status, (
            #     f"Ожидался {expected_status}, получен {response.status_code}"
            # )
            # assert "Превышена длина! in response.json().get("message", ""), (
            #     f"Неверное сообщение: {response.json()}"
            # )