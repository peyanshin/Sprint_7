"""Тестовые данные для API создания курьера."""


# Базовые данные для заказа (без цвета)
BASE_ORDER_PAYLOAD = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": 4,
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2020-06-06",
    "comment": "Saske, come back to Konoha"
}

# Варианты payloads для заказов с разными цветами
ORDER_PAYLOADS = {
    "black": {**BASE_ORDER_PAYLOAD, "color": ["BLACK"]},
    "grey": {**BASE_ORDER_PAYLOAD, "color": ["GREY"]},
    "both": {**BASE_ORDER_PAYLOAD, "color": ["BLACK", "GREY"]},
    "no_color": BASE_ORDER_PAYLOAD
}

# Константы для генерации курьеров
LOGIN_PREFIX = "test_ninja_"
DEFAULT_PASSWORD = "1234"
DEFAULT_FIRST_NAME = "Sasuke"


# Валидные данные для создания курьера
VALID_COURIER = {
    "login": "{timestamp}_{suffix}",
    "password": DEFAULT_PASSWORD,
    "firstName": DEFAULT_FIRST_NAME
}

# Данные без обязательных полей
MISSING_FIELDS = {
    "login": {"password": DEFAULT_PASSWORD, "firstName": DEFAULT_FIRST_NAME},
    "password": {"login": "{timestamp}_{suffix}", "firstName": DEFAULT_FIRST_NAME},
    "firstName": {"login": "{timestamp}_{suffix}", "password": DEFAULT_PASSWORD}
}

# Пустые значения полей
EMPTY_FIELDS = {
    "login": "",
    "password": "",
    "firstName": ""
}

# Граничные значения (очень длинные/короткие строки)
BOUNDARY_VALUES = {
    "login": "a",  # минимальная длина
    "password": "x" * 100,  # максимальная длина
    "firstName": "X" * 100  # максимальная длина
}

# Сообщения об ошибках
ERROR_MESSAGES = {
    "missing_data": "Недостаточно данных для создания учётной записи",
    "duplicate_login": "Этот логин уже используется. Попробуйте другой.",
    "missing_fields": "Недостаточно данных для входа",
    "account_not_found": "Учетная запись не найдена"
}

# Сообщения об ошибках (для авторизации)
AUTH_ERROR_MESSAGES = {
    "missing_fields": "Недостаточно данных для входа",
    "account_not_found": "Учетная запись не найдена"
}

# Ожидаемые статусы ответов
EXPECTED_STATUS_CODES = {
    "success": 200,
    "created": 201,
    "bad_request": 400,
    "not_found": 404
}

# Шаблоны сообщений для проверок статуса ответа
STATUS_ERROR_MESSAGES = {
    "success": "Ожидался статус {expected}, получен {actual}",
    "bad_request": "Ожидался статус {expected}, получен {actual}",
    "not_found": "Ожидался статус {expected}, получен {actual}",
    "create_order": "Ожидался статус {expected}, получен {actual}. Ответ: {response_text}",
    "get_orders": "Ожидался статус {expected}, получен {actual}. Ответ: {response_text}"

}

# Сообщения для assert-проверкок в тестах
ASSERT_MESSAGES = {
    "missing_id": "В ответе отсутствует поле 'id'",
    "invalid_id_type": "Поле 'id' должно быть целым числом",
    "missing_track": "В ответе отсутствует поле 'track'",
    "missing_orders": "В ответе отсутствует список заказов (поле 'orders')",
    "invalid_orders_type": "Поле 'orders' не является списком"

}

