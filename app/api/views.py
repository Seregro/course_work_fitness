from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models import *

router = APIRouter(tags=["Views"])
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def index(user: User = Depends(get_current_user)):
    if not user: return RedirectResponse(url="/login")
    if user.role == UserRole.CLIENT: return RedirectResponse(url="/me")
    return RedirectResponse(url="/admin/dashboard")

@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/admin/dashboard")
async def dashboard(request: Request, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    if not user or user.role == UserRole.CLIENT: return RedirectResponse(url="/login")
    
    stats = {
        "clients": await db.scalar(select(func.count(Client.id))),
        "trainers": await db.scalar(select(func.count(Trainer.id))),
        "sales": await db.scalar(select(func.sum(Sale.price * Sale.quantity))) or 0
    }
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "stats": stats})

@router.get("/me")
async def client_me(request: Request, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    if not user: return RedirectResponse(url="/login")
    
    # Данные клиента
    client = (await db.execute(select(Client).where(Client.user_id == user.id))).scalar_one()
    subs = (await db.execute(select(Subscription).where(Subscription.client_id == client.id).options(selectinload(Subscription.sub_type)))).scalars().all()
    visits = (await db.execute(select(VisitLog).where(VisitLog.client_id == client.id).limit(10))).scalars().all()
    
    return templates.TemplateResponse("client_me.html", {
        "request": request, "user": user, "client": client, "subscriptions": subs, "visits": visits
    })

@router.get("/book")
async def client_booking(request: Request, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    if not user: return RedirectResponse(url="/login")
    res = await db.execute(select(Schedule).options(selectinload(Schedule.workout_type), selectinload(Schedule.trainer).selectinload(Trainer.user), selectinload(Schedule.gym)))
    return templates.TemplateResponse("client_booking.html", {"request": request, "user": user, "classes": res.scalars().all()})

@router.get("/admin/dashboard")
async def dashboard(
    request: Request, 
    db: AsyncSession = Depends(get_db), 
    user: User = Depends(get_current_user)
):
    # Если пользователь не найден или он клиент — не пускаем в админку
    if not user or user.role == UserRole.CLIENT:
        print("DEBUG: Access denied to dashboard, redirecting to login")
        return RedirectResponse(url="/login", status_code=303)

    # ... остальной код (stats и т.д.) ...
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "user": user, 
        "stats": stats
    })