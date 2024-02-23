from app.extensions import Base, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from uuid import uuid4, UUID


class FormQuestionResponse(Base):
  id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
  response: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)  
  question_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('question.id'), unique=False, nullable=False)
  
  def __init__(self, user_id: UUID, company_id: UUID, area_id: UUID, question_id: UUID, answer: str):
    self.user_id = user_id
    self.company_id = company_id
    self.area_id = area_id
    self.question_id = question_id
    self.answer = answer