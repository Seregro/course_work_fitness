from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.subscription import Subscription
from app.models.visit_log import VisitLog
from app.models.sale import Sale
from datetime import datetime

router = APIRouter(prefix="/ops", tags=["operations"])

@router.post("/check-in/{client_id}")
async def check_in(client_id: int, locker_id: int, db: AsyncSession = Depends(get_db)):
    # Логика: проверить активный абонемент и создать запись в VisitLog
    visit = VisitLog(client_id=client_id, locker_id=locker_id, check_in=datetime.utcnow())
    db.add(visit)
    await db.commit()
    return {"status": "checked in", "visit_id": visit.id}

@router.post("/sale")
async def process_sale(item: str, price: float, seller_id: int, db: AsyncSession = Depends(get_db)):
    sale = Sale(item_name=item, price=price, seller_id=seller_id)
    db.add(sale)
    await db.commit()
    return {"status": "sold", "item": item}