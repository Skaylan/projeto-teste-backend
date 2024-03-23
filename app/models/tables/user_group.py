from app.extensions import Base, db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from uuid import uuid4, UUID


class UserGroup(Base):
  id: Mapped[UUID] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
  user_id: Mapped[UUID] = mapped_column(String(36), ForeignKey("user.id"), nullable=False)
  group_id: Mapped[UUID] = mapped_column(String(36), ForeignKey("group.id"), nullable=False)
  
  def __init__(self, user_id: UUID, group_id: UUID):
    self.user_id = user_id
    self.group_id = group_id