from app.extensions import Base, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer
from uuid import uuid4, UUID


class FormQuestionResponse(Base):
  id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
  form_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('form_diagnostic.id'), unique=True, nullable=False)
  question_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('question.id'), unique=True, nullable=False)
  response: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)  
  
  def __init__(self, user_id: UUID, company_id: UUID, area_id: UUID, question_id: UUID, answer: str, form_diagnotic_id: UUID):
    self.user_id = user_id
    self.company_id = company_id
    self.area_id = area_id
    self.question_id = question_id
    self.answer = answer
    self.form_diagnotic_id = form_diagnotic_id