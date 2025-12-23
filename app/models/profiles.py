from sqlalchemy import String, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from datetime import date

class Client(Base):
    __tablename__ = "clients"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    phone: Mapped[str] = mapped_column(String(20))
    birth_date: Mapped[date] = mapped_column(Date, nullable=True)
    card_number: Mapped[str] = mapped_column(String(50), unique=True)

    user: Mapped["User"] = relationship()

class Trainer(Base):
    __tablename__ = "trainers"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    specialization: Mapped[str] = mapped_column(String(255))
    experience_years: Mapped[int] = mapped_column(default=0)
    bio: Mapped[str] = mapped_column(String(1000), nullable=True)

    user: Mapped["User"] = relationship()