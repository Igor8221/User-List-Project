import uuid

from typing import Optional
"""  Тип, предоставляемый модулем typing, который указывает, что переменная может быть типа None """
from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    login: str
    """ добавление поля login для схемы fastapi_users """


class UserCreate(schemas.BaseUserCreate):
    login: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = True
    is_verified: Optional[bool] = True


class UserUpdate(schemas.BaseUserUpdate):
    login: str
