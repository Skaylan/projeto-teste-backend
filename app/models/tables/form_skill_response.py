from app.extensions import Base, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
from uuid import uuid4, UUID


class FormSkillResponse(Base):
  id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
  form_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('form_diagnostic.id'), unique=True, nullable=False)
  skill_id: Mapped[int] = mapped_column(Integer, ForeignKey('skill.id'), unique=True, nullable=False)
  order: Mapped[int] = mapped_column(Integer, unique=False, nullable=False)
  
  
  def __init__(self, form_id: UUID, skill_id: UUID, order: int):
    self.form_id = form_id
    self.skill_id = skill_id
    self.order = order