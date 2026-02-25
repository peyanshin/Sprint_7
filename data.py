
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

ORDER_PAYLOADS = {
    "black": {**BASE_ORDER_PAYLOAD, "color": ["BLACK"]},
    "grey": {**BASE_ORDER_PAYLOAD, "color": ["GREY"]},
    "both": {**BASE_ORDER_PAYLOAD, "color": ["BLACK", "GREY"]},
    "no_color": BASE_ORDER_PAYLOAD
}


EXPECTED_STATUS_CODES = {
    "success": 200,
    "created": 201,
    "bad_request": 400,
    "not_found": 404,
    "conflict": 409
}


ERROR_MESSAGES = {
    "missing_data": "Недостаточно данных для создания учётной записи",
    "duplicate_login": "Этот логин уже используется. Попробуйте другой.",
    "missing_fields": "Недостаточно данных для входа",
    "account_not_found": "Учетная запись не найдена",
    "success": "Ожидался статус {expected}, получен {actual}",
    "bad_request": "Ожидался статус {expected}, получен {actual}",
    "not_found": "Ожидался статус {expected}, получен {actual}",
    "create_order": "Ожидался статус {expected}, получен {actual}. Ответ: {response_text}",
    "get_orders": "Ожидался статус {expected}, получен {actual}. Ответ: {response_text}",
    "unexpected_error_message": "Неверное сообщение об ошибке: {actual_message}",
    "create_courier_success_response": {"ok": True},
    "create_courier_missing_login_message": "Недостаточно данных",
    "create_courier_missing_password_message": "Недостаточно данных",
    "create_identical_couriers_message": "Этот логин уже используется. Попробуйте другой."
}


ASSERT_MESSAGES = {
    "missing_id": "В ответе отсутствует поле 'id'",
    "invalid_id_type": "Поле 'id' должно быть целым числом",
    "missing_track": "В ответе отсутствует поле 'track'",
    "missing_orders": "В ответе отсутствует список заказов (поле 'orders')",
    "invalid_orders_type": "Поле 'orders' не является списком",


    "create_courier_success_status": "Ожидался статус 201, получен {actual}: {response_text}",
    "create_courier_success_json": "Ответ должен быть {'ok': True}",
    "auth_courier_failure": "Курьер не может авторизоваться: {response_text}",
    "missing_id_in_auth": "В ответе авторизации отсутствует id курьера",
    "create_courier_missing_field_status": "Ожидался 400, получен {actual}: {response_text}",
    "incorrect_error_message": "Неверное сообщение: {response_json}",
    "create_identical_couriers_status": "Ожидался 409 (конфликт из‑за дублирующего логина), получен {actual}: {response_text}",
    "incorrect_conflict_message": "Неверное сообщение об ошибке. Ожидалось: '{expected}', получено: {actual}"
}


LOGIN_PREFIX = "test_ninja_"
DEFAULT_PASSWORD = "1234"
DEFAULT_FIRST_NAME = "Sasuke"



VALID_COURIER = {
    "login": "{timestamp}_{suffix}",
    "password": DEFAULT_PASSWORD,
    "firstName": DEFAULT_FIRST_NAME
}

MISSING_FIELDS = {
    "login": {"password": DEFAULT_PASSWORD, "firstName": DEFAULT_FIRST_NAME},
    "password": {"login": "{timestamp}_{suffix}", "firstName": DEFAULT_FIRST_NAME},
    "firstName": {"login": "{timestamp}_{suffix}", "password": DEFAULT_PASSWORD}
}

EMPTY_FIELDS = {
    "login": "",
    "password": "",
    "firstName": ""
}

BOUNDARY_VALUES = {
    "login": "a",  
    "password": "x" * 100,  
    "firstName": "X" * 100  
}

MISSING_ALL_FIELDS = {}  

CASE_INSENSITIVE_LOGIN = {
    "login": "TestLogin123",
    "password": DEFAULT_PASSWORD,
    "firstName": DEFAULT_FIRST_NAME
}

MISSING_LOGIN = {
    "password": DEFAULT_PASSWORD,
    "firstName": DEFAULT_FIRST_NAME
}

MISSING_PASSWORD = {
    "login": "{timestamp}_{suffix}",
    "firstName": DEFAULT_FIRST_NAME
}

MISSING_FIRSTNAME = {
    "login": "{timestamp}_{suffix}",
    "password": DEFAULT_PASSWORD
}
