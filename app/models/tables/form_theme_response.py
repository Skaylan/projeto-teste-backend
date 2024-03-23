from app.extensions import db, Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
from uuid import uuid4, UUID


class FormThemeResponse(Base):
  id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
  form_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('form_diagnostic.id'), unique=True, nullable=False)
  theme_id: Mapped[int] = mapped_column(Integer, ForeignKey('theme.id'), unique=True, nullable=False)
  order: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
  
  def __init__(self, form_id: UUID, theme_id: UUID, order: int):
    self.form_id = form_id
    self.theme_id = theme_id
    self.order = order