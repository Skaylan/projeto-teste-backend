from app.extensions import Base, db
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from sqlalchemy import String, ForeignKey
from uuid import uuid4


class UserCompany(Base):
    id = db.Column(String(36), primary_key=True, default=lambda: str(uuid4()))
    company_id: Mapped[str] = mapped_column(String(36), ForeignKey('company.id'), unique=False, nullable=False)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey('user.id'), unique=False, nullable=False)

    def __init__(self, company_id: str, user_id: str):
        self.company_id = company_id
        self.user_id = user_id