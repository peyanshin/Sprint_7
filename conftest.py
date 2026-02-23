import pytest
import time
import random

from url import *
from api_methods.create_courier_method import *



def generate_unique_data(template: dict) -> dict:
    """Генерирует уникальные данные с timestamp и случайным суффиксом."""
    timestamp = int(time.time() * 1000)
    random_suffix = str(random.randint(100000, 999999))

    return {
        key: (
            value.format(timestamp=timestamp, suffix=random_suffix)
            if isinstance(value, str) and ("{timestamp}" in value or "{suffix}" in value)
            else value
        )
        for key, value in template.items()
    }



def generate_unique_login() -> str:
    """Генерирует гарантированно уникальный логин."""
    while True:
        timestamp = int(time.time() * 1000)
        random_suffix = str(random.randint(100000, 999999))
        login = f"test_ninja_{timestamp}_{random_suffix}"
        if len(login) <= 50:
            return login



@pytest.fixture(scope="class")
def setup_cleanup():
    """Очищает тестовых курьеров перед запуском тестов класса."""
    cleanup_test_couriers("test_ninja_")
    yield



@pytest.fixture(scope="function")
def courier_credentials():
    """Фикстура для генерации временных данных курьера."""
    timestamp = int(time.time() * 1000)
    login = f"test_ninja_{timestamp}"
    password = "secure_pass_123"
    first_name = "TestSasuke"
    return login, password, first_name

@pytest.fixture(scope="function")
def created_courier(courier_credentials):
    """
    Фикстура для создания курьера перед тестом и его удаления после.
    Гарантирует очистку даже при падении теста.
    """
    login, password, first_name = courier_credentials
    response = create_courier(login, password, first_name)
    assert response.status_code == 201, f"Не удалось создать курьера: {response.text}"

    try:
        yield login, password  
    finally:
        success = delete_courier(login, password)
        if not success:
            print(f"Предупреждение: не удалось удалить курьера с логином {login}")
