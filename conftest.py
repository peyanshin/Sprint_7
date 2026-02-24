import pytest

from helpers import *

@pytest.fixture(scope="function")
def courier_credentials():
    """Фикстура для генерации временных данных курьера (только данные, без создания)."""
    login = generate_unique_login()
    password = "secure_pass_123"
    first_name = "TestSasuke"
    return login, password, first_name

@pytest.fixture(scope="function")
def created_courier(courier_credentials):
    """Фикстура для создания курьера перед тестом и его удаления после. Гарантирует очистку даже при падении теста."""
    login, password, first_name = courier_credentials
    response = create_courier(login, password, first_name)
    assert response.status_code == 201, f"Не удалось создать курьера: {response.text}"
    yield login, password
    delete_courier(login, password)
