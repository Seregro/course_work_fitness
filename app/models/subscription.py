from sqlalchemy import ForeignKey, Date, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from datetime import date

class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    type_id: Mapped[int] = mapped_column(ForeignKey("subscription_types.id"))
    start_date: Mapped[date] = mapped_column(Date, default=date.today)
    end_date: Mapped[date] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    client: Mapped["Client"] = relationship()
    sub_type: Mapped["SubscriptionType"] = relationship()