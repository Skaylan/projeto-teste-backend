from app.extensions import Base, db
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy import String
from uuid import uuid4

class Company(Base):
    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    cnpj: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    company_name: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    trading_name: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    address: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
    city: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    state: Mapped[str] = mapped_column(String(500), unique=False, nullable=False)
    phone: Mapped[str] = mapped_column(String(45), unique=False, nullable=False)
    
    
    def __init__(
      self, 
      cnpj: str,
      email: str,
      company_name: str, 
      trading_name: str, 
      address: str, 
      city: str, 
      state: str, 
      phone: str
    ):
        self.cnpj = cnpj
        self.company_name = company_name
        self.trading_name = trading_name
        self.address = address
        self.city = city
        self.state = state
        self.phone = phone