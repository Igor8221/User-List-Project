import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from src.database import User
from src.auth import auth_backend
from src.schemas import UserCreate, UserRead, UserUpdate
from src.user_manager import get_user_manager


router = APIRouter(prefix='/auth')
""" Создается экземпляр APIRouter с префиксом /auth. все маршруты, включенные в этот маршрутизатор, будут иметь URL, начинающийся с /auth """

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
""" User: Модель пользователя, определенная в базе данных.
uuid.UUID: Тип идентификатора пользователя.
get_user_manager: Функция, которая возвращает менеджера пользователей.
[auth_backend]: Список аутентификационных бекендов """ 

""" Маршрут аутентификации """
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

""" Маршрут регистрации """
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/reg",
    tags=["auth"],
)

""" Маршрут управления пользователями """
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
