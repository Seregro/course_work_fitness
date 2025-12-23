from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class Gym(Base):
    __tablename__ = "gyms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    capacity: Mapped[int] = mapped_column(default=20)