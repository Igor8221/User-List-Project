from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
    JWTStrategy
)
""" SECRET - это строка, которая используется для подписи JWT """
SECRET = "SECRET"

""" определяется транспортный слой, который использует куки для хранения токенов """
cookie_transport = CookieTransport(cookie_max_age=3600)

""" Функция get_jwt_strategy возвращает экземпляр JWTStrategy, который используется для создания и проверки JWT """
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

""" auth_backend - это экземпляр AuthenticationBackend, который объединяет транспортный слой и стратегию аутентификации """
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)
