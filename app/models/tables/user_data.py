from app.extensions import Base, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from uuid import uuid4, UUID


class UserData(Base):
  id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
  user_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('user.id'), unique=False, nullable=False)
  cpf: Mapped[str] = mapped_column(String(50), unique=False, nullable=False)
  phone: Mapped[str] = mapped_column(String(45), unique=False, nullable=False)
  address: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
  city: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
  state: Mapped[str] = mapped_column(String(500), unique=False, nullable=False)
  
  
  def __init__(self, user_id: UUID, cpf: str, phone: str, address: str, city: str, state: str):
    self.user_id = user_id
    self.cpf = cpf
    self.phone = phone
    self.address = address
    self.city = city
    self.state = state