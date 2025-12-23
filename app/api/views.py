from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.db.session import get_db
from app.models import Client, User, Trainer, Gym, Schedule, WorkoutType, SubscriptionType, VisitLog, Sale, Subscription, Locker

router = APIRouter(tags=["Frontend Views"])
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    clients_count = await db.scalar(select(func.count(Client.id)))
    trainers_count = await db.scalar(select(func.count(Trainer.id)))
    sales_sum = await db.scalar(select(func.sum(Sale.price * Sale.quantity)))
    
    # Ближайшие занятия с подгрузкой отношений
    sched_result = await db.execute(
        select(Schedule).options(
            selectinload(Schedule.workout_type),
            selectinload(Schedule.trainer).selectinload(Trainer.user),
            selectinload(Schedule.gym)
        ).order_by(Schedule.start_time).limit(5)
    )
    upcoming_classes = sched_result.scalars().all()
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "stats": {"clients": clients_count or 0, "trainers": trainers_count or 0, "sales": sales_sum or 0},
        "upcoming_classes": upcoming_classes
    })

@router.get("/clients")
async def clients_page(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Client).options(selectinload(Client.user)))
    clients = result.scalars().all()
    return templates.TemplateResponse("clients.html", {"request": request, "clients": clients})

@router.get("/schedule")
async def schedule_page(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Schedule).options(
            selectinload(Schedule.workout_type),
            selectinload(Schedule.trainer).selectinload(Trainer.user),
            selectinload(Schedule.gym)
        )
    )
    schedules = result.scalars().all()
    return templates.TemplateResponse("schedule.html", {"request": request, "schedules": schedules})

@router.get("/reports") # Исправили 404
async def reports_page(request: Request, db: AsyncSession = Depends(get_db)):
    gyms = (await db.execute(select(Gym))).scalars().all()
    sub_types = (await db.execute(select(SubscriptionType))).scalars().all()
    sales = (await db.execute(select(Sale))).scalars().all()
    return templates.TemplateResponse("reports.html", {
        "request": request, "gyms": gyms, "sub_types": sub_types, "sales": sales
    })

@router.get("/visits")
async def visits_page(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(VisitLog).options(
            selectinload(VisitLog.client).selectinload(Client.user),
            selectinload(VisitLog.locker)
        ).order_by(VisitLog.check_in.desc())
    )
    visits = result.scalars().all()
    lockers = (await db.execute(select(Locker))).scalars().all()
    return templates.TemplateResponse("visits.html", {"request": request, "visits": visits, "lockers": lockers})

@router.get("/sales")
async def sales_page(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Sale).order_by(Sale.sold_at.desc()))
    sales = result.scalars().all()
    return templates.TemplateResponse("sales.html", {"request": request, "sales": sales})

@router.get("/subscriptions")
async def subscriptions_page(request: Request, db: AsyncSession = Depends(get_db)):
    # Получаем активные абонементы со всеми связями
    result = await db.execute(
        select(Subscription).options(
            selectinload(Subscription.client).selectinload(Client.user),
            selectinload(Subscription.sub_type)
        )
    )
    subs = result.scalars().all()
    clients = (await db.execute(select(Client).join(User))).scalars().all()
    types = (await db.execute(select(SubscriptionType))).scalars().all()
    
    return templates.TemplateResponse("subscriptions.html", {
        "request": request, "subs": subs, "clients": clients, "sub_types": types
    })