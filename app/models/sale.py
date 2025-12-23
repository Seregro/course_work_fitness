from sqlalchemy import String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base
from datetime import datetime

class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_name: Mapped[str] = mapped_column(String(100))
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    quantity: Mapped[int] = mapped_column(default=1)
    sold_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"))