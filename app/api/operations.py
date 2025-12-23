from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from app.db.session import get_db
from app.models import Sale, Client, Locker, VisitLog, Subscription, SubscriptionType
from datetime import datetime, timedelta

router = APIRouter(prefix="/ops", tags=["Operations"])

@router.post("/sale")
async def process_sale(
    item_name: str = Form(...),
    price: float = Form(...),
    quantity: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # В реальности тут должен быть ID текущего юзера (продавца)
    new_sale = Sale(item_name=item_name, price=price, quantity=quantity, seller_id=1) 
    db.add(new_sale)
    await db.commit()
    return RedirectResponse(url="/sales", status_code=303)

@router.post("/check-in")
async def check_in(
    client_id: int = Form(...),
    locker_id: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Проверяем, свободен ли шкафчик
    locker = await db.get(Locker, locker_id)
    if locker.is_occupied:
        raise HTTPException(status_code=400, detail="Locker occupied")
    
    # Создаем визит и занимаем шкафчик
    visit = VisitLog(client_id=client_id, locker_id=locker_id)
    locker.is_occupied = True
    db.add(visit)
    await db.commit()
    return RedirectResponse(url="/visits", status_code=303)

@router.post("/add-subscription")
async def add_sub(
    client_id: int = Form(...),
    type_id: int = Form(...),
    db: AsyncSession = Depends(get_db)
):
    sub_type = await db.get(SubscriptionType, type_id)
    new_sub = Subscription(
        client_id=client_id,
        type_id=type_id,
        start_date=datetime.now().date(),
        end_date=(datetime.now() + timedelta(days=sub_type.duration_days)).date()
    )
    db.add(new_sub)
    await db.commit()
    return RedirectResponse(url="/subscriptions", status_code=303)