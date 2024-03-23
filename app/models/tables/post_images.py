from app.extensions import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from uuid import uuid4, UUID


class PostImages(Base):
  id: Mapped[UUID] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
  image_uuid: Mapped[UUID] = mapped_column(String(36), unique=True, nullable=False)
  post_id: Mapped[UUID] = mapped_column(String(36), ForeignKey("post.id"), unique=True, nullable=False)
  
  def __init__(self, image_uuid: UUID, post_id: UUID):
    self.image_uuid = image_uuid
    self.post_id = post_id