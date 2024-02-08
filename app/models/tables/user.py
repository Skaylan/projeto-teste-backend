from app.config.app_config import *
from app.config.db_config import *
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Text
from uuid import uuid4, UUID


class User(Base):
    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(45), unique=False, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(256), unique=False, nullable=False)
    user_type_id: Mapped[UUID] = mapped_column(String(36), ForeignKey('user_type.id'), unique=False, nullable=False)

    def __init__(self, name: str, email:str, password_hash: str, user_type_id: UUID):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.user_type_id = user_type_id