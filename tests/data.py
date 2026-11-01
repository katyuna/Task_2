# URLs
BASE_URL = "https://stellarburgers.education-services.ru/api"

REGISTER_URL = f"{BASE_URL}/auth/register"  # создание пользователя
LOGIN_URL = f"{BASE_URL}/auth/login"  # логин
USER_URL = f"{BASE_URL}/auth/user"  # получить, изменить и удалить пользователя
INGREDIENTS_URL = f"{BASE_URL}/ingredients"  # список ингредиентов
ORDERS_URL = f"{BASE_URL}/orders"  # создать заказ и получить заказы пользователя

# ERRORS
USER_ALREADY_EXISTS = "User already exists"
REQUIRED_FIELDS_MISSING = "Email, password and name are required fields"
INCORRECT_CREDENTIALS = "email or password are incorrect"
UNAUTHORISED = "You should be authorised"
NO_INGREDIENTS = "Ingredient ids must be provided"
