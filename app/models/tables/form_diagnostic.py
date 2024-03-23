from app.extensions import Base, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Boolean, Integer
from uuid import uuid4, UUID


class FormDiagnostic(Base):
    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('user.id'), unique=False, nullable=False)
    company_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('company.id'), unique=False, nullable=False)
    area_id: Mapped[Integer] = mapped_column(Integer, ForeignKey('area.id'), unique=False, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, unique=False, nullable=False)
    
  
    def __init__(self, user_id: UUID, company_id: UUID, area_id: int):
        self.user_id = user_id
        self.company_id = company_id
        self.area_id = area_id
        
  