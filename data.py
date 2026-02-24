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

# Заказ с цветом BLACK
ORDER_WITH_BLACK_COLOR = {**BASE_ORDER_PAYLOAD, "color": ["BLACK"]}

# Заказ с цветом GREY
ORDER_WITH_GREY_COLOR = {**BASE_ORDER_PAYLOAD, "color": ["GREY"]}

# Заказ с обоими цветами
ORDER_WITH_BOTH_COLORS = {**BASE_ORDER_PAYLOAD, "color": ["BLACK", "GREY"]}

# Заказ без указания цвета (то же, что BASE_ORDER_PAYLOAD)
ORDER_WITHOUT_COLOR = BASE_ORDER_PAYLOAD

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

# Данные без поля login
MISSING_LOGIN = {
    "password": DEFAULT_PASSWORD,
    "firstName": DEFAULT_FIRST_NAME
}

# Данные без поля password
MISSING_PASSWORD = {
    "login": "{timestamp}_{suffix}",
    "firstName": DEFAULT_FIRST_NAME
}

# Данные без поля firstName
MISSING_FIRSTNAME = {
    "login": "{timestamp}_{suffix}",
    "password": DEFAULT_PASSWORD
}

# Пустые значения полей
EMPTY_FIELDS = {
    "login": "",
    "password": "",
    "firstName": ""
}

# Граничные значения (очень длинные/короткие строки)
BOUNDARY_VALUES = {
    "login": "a",
    "password": "x" * 100,
    "firstName": "X" * 100 
}

# Сообщения об ошибках (для создания учётной записи)
ERROR_MESSAGES = {
    "missing_data": "Недостаточно данных для создания учётной записи",
    "duplicate_login": "Этот логин уже используется. Попробуйте другой."
}

# Сообщения об ошибках (для авторизации)
AUTH_ERROR_MESSAGES = {
    "missing_fields": "Недостаточно данных для входа",
    "account_not_found": "Учетная запись не найдена"
}

# Ожидаемые статусы ответов
EXPECTED_STATUS_CODES = {
    "success": 200,
    "bad_request": 400,
    "not_found": 404
}

# Шаблоны сообщений для проверок статуса ответа
STATUS_ERROR_MESSAGES = {
    "success": "Ожидался статус {expected}, получен {actual}",
    "bad_request": "Ожидался статус {expected}, получен {actual}",
    "not_found": "Ожидался статус {expected}, получен {actual}"
}

# Сообщения для assert-проверкок в тестах
ASSERT_MESSAGES = {
    "missing_id": "В ответе отсутствует поле 'id'",
    "invalid_id_type": "Поле 'id' должно быть целым числом"
}
