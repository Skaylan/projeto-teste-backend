from app.extensions import Base, db
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy import String, Integer
from uuid import uuid4

class UserType(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    descr: Mapped[str] = mapped_column(String(45), unique=False, nullable=False)
    owner_id = relationship('User', backref='user_type')
    
    
    def __init__(self, descr: str):
        self.descr = descr