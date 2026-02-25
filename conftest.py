import pytest

from helpers import *


@pytest.fixture(scope="function")
def courier_credentials():
    """Генерация временных данных без создания курьера"""
    login = generate_unique_login()
    password = "secure_pass_123"
    first_name = "TestSasuke"
    return login, password, first_name

@pytest.fixture(scope="function")
def created_courier(courier_credentials):
    """Создание курьера перед тестом и его удаление после"""
    login, password, first_name = courier_credentials
    response = create_courier(login, password, first_name)
    yield login, password, response
    delete_courier(login, password)
