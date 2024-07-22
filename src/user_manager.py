import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin, models, schemas, exceptions

from src.database import User, get_user_db

SECRET = "SECRET"

""" UserManager наследуется от UUIDIDMixin и BaseUserManager """
""" UUIDIDMixin: Миксин, который добавляет поддержку UUID как идентификаторов пользователей. """
""" BaseUserManager: Базовый класс для управления пользователями."""

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):      
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET
    
    """  Метод для создания пользователя """
    
    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        
        """ проверка пароля на соответствие """
        await self.validate_password(user_create.password, user_create)                 

        """ Проверка, существует ли пользователь с таким же email """
        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()
        
        """ Преобразование объекта user_create в словарь. """
        """ Хэширование пароля и сохранение его в поле hashed_password. """
        """ Установка полей is_verified, is_superuser и is_active в True. """
        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict['is_verified'] = True
        user_dict['is_superuser'] = True
        user_dict['is_active'] = True
        
        """ Создание пользователя в базе данных. """
        created_user = await self.user_db.create(user_dict)

        """ Вызов хука on_after_register, который выполняется после регистрации пользователя. Можно использовать для отправки подтверждающих писем и других действий. """
        await self.on_after_register(created_user, request)
        
        """ Возврат пользователя """
        return created_user

""" Функция get_user_manager: Предоставляет экземпляр менеджера пользователя для внедрения зависимостей в FastAPI """
async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
