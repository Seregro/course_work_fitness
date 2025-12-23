from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse  # ВОТ ЭТОГО ИМПОРТА НЕ ХВАТАЛО
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models import Schedule, Client, User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def home(request: Request, user = Depends(get_current_user), db = Depends(get_db)):
    if not user:
        # Если юзера нет в deps, кидаем на логин
        return RedirectResponse(url="/login", status_code=303)
    
    # Пытаемся найти клиента
    from app.models import Client
    res = await db.execute(select(Client).where(Client.user_id == user.id))
    client = res.scalar_one_or_none()
    
    return templates.TemplateResponse("index.html", {"request": request, "user": user, "client": client})

@router.get("/login")
async def login_pg(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register")
async def reg_pg(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/schedule")
async def schedule_pg(request: Request, user=Depends(get_current_user), db: AsyncSession=Depends(get_db)):
    if not user: 
        return RedirectResponse(url="/login", status_code=303)
    
    # Загружаем расписание вместе с типами тренировок
    res = await db.execute(select(Schedule).options(selectinload(Schedule.workout_type)))
    return templates.TemplateResponse("schedule.html", {
        "request": request, 
        "classes": res.scalars().all()
    })