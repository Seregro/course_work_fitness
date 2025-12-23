from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base
from datetime import datetime

class VisitLog(Base):
    __tablename__ = "visit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    locker_id: Mapped[int] = mapped_column(ForeignKey("lockers.id"), nullable=True)
    check_in: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    check_out: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    client: Mapped["Client"] = relationship()
    locker: Mapped["Locker"] = relationship()