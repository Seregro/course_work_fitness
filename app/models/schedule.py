from sqlalchemy import ForeignKey, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from datetime import datetime

class Schedule(Base):
    __tablename__ = "schedule"

    id: Mapped[int] = mapped_column(primary_key=True)
    workout_type_id: Mapped[int] = mapped_column(ForeignKey("workout_types.id"))
    trainer_id: Mapped[int] = mapped_column(ForeignKey("trainers.id"))
    gym_id: Mapped[int] = mapped_column(ForeignKey("gyms.id"))
    start_time: Mapped[datetime] = mapped_column(DateTime)
    end_time: Mapped[datetime] = mapped_column(DateTime)
    max_participants: Mapped[int] = mapped_column(Integer)

    workout_type: Mapped["WorkoutType"] = relationship()
    trainer: Mapped["Trainer"] = relationship()
    gym: Mapped["Gym"] = relationship()