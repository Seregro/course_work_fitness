from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base

class SubscriptionType(Base):
    __tablename__ = "subscription_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    duration_days: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    visit_limit: Mapped[int] = mapped_column(nullable=True)