from app.extensions import Base, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from uuid import uuid4, UUID


class Area(Base):
  id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
  descr: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
  active: Mapped[bool] = mapped_column(Boolean, default=True, unique=False, nullable=False)
  
  
  def __init__(self, descr: str):
    self.descr = descr