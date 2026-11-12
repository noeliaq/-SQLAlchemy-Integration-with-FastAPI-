#app/models/notes.py

from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Note(Base):
    __tablename__ = "Notes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(nullable= False)
    category: Mapped[Optional[str]] = mapped_column(String(50))
    is_pinned: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now()) #default current date and time if there is no value.