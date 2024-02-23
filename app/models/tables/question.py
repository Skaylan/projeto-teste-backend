from app.extensions import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean
from uuid import uuid4, UUID


class Question(Base):
  id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
  type: Mapped[str] = mapped_column(String(10), unique=False, nullable=False)
  order: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
  descr: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
  response_options: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
  active: Mapped[bool] = mapped_column(Boolean, default=True, unique=False, nullable=False)
  
  
  def __init__(self, type: str, order: int, descr: str, response_options: str):
    self.type = type
    self.order = order
    self.descr = descr
    self.response_options = response_options
    