import uuid

from fastapi_users import FastAPIUsers

from sqlalchemy import select
from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from src.auth import auth_backend
from src.user_manager import get_user_manager
from src.database import async_session_maker, User


router = APIRouter()
templates = Jinja2Templates(directory='templates')

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user(optional=True)


@router.get('/')
async def show_homepage(request: Request, user = Depends(current_user), q: str = None):
    """ user=Depends(current_user) зависимость, которая извлекает текущего пользователя (получение данных) если пользователь аутентифицирован, иначе None """
    
    context = {'cur_user': user, "q": q}
    """ Создается словарь context, содержащий текущего пользователя (cur_user) и строку поиска (q). """
    async with async_session_maker() as session:
        """ Открывается асинхронная сессия для взаимодействия с базой данных """
        if not q:
            query = select(User)
        else:
            query = select(User).where(User.login.like('%{}%'.format(q)))
        """ Если строка поиска (q) не указана, выбираются все пользователи (select(User)). """
        """ Если строка поиска указана, выбираются пользователи, чьи логины содержат подстроку q """
        users = await session.execute(query)
        users = [row[0] for row in users.all()]
        """ Запрос выполняется асинхронно (await session.execute(query)). """
        """ Результаты преобразуются в список объектов пользователей """
        context.update({'users': users})
        """ В контекст добавляется список пользователей. """

        return templates.TemplateResponse(request=request, name='home_page.html', context=context)


@router.get('/about')
def show_aboutpage(request: Request, user = Depends(current_user)):
    context = {'cur_user': user}
    return templates.TemplateResponse(request=request, name='about_page.html', context=context)


@router.get('/registration')
async def show_registration(request: Request, user = Depends(current_user)):
    context = {'cur_user': user}
    return templates.TemplateResponse(request=request, name='registration.html', context=context)


@router.get('/login')
async def show_login(request: Request, user = Depends(current_user)):
    context = {'cur_user': user}
    return templates.TemplateResponse(request=request, name='login.html', context=context)

@router.get('/logout')
async def show_login(request: Request, user = Depends(current_user)):
    context = {'cur_user': user}
    return templates.TemplateResponse(request=request, name='logout.html', context=context)