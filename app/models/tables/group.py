from app.extensions import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Text, Integer
from uuid import uuid4, UUID


class Group(Base):
  id: Mapped[UUID] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
  name: Mapped[str] = mapped_column(String(255), unique=False, nullable=False)
  descr: Mapped[str] = mapped_column(Text, unique=False, nullable=True)
  user_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('user.id'), unique=False, nullable=False)
  custom_theme_id: Mapped[int] = mapped_column(Integer, ForeignKey('group_custom_theme.id'), unique=False, nullable=False)
  
  def __init__(self, name: str, descr: str, user_id: UUID, custom_theme_id: int):
    self.name = name
    self.descr = descr
    self.user_id = user_id
    self.custom_theme_id = custom_theme_id