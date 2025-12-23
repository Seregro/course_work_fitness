from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.gym import Gym
from app.models.workout import WorkoutType

router = APIRouter(prefix="/gyms", tags=["gyms"])

@router.get("/")
async def list_gyms(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Gym))
    return result.scalars().all()

@router.post("/")
async def create_gym(name: str, cap: int, db: AsyncSession = Depends(get_db)):
    new_gym = Gym(name=name, capacity=cap)
    db.add(new_gym)
    await db.commit()
    return new_gym