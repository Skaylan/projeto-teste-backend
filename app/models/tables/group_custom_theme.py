from app.extensions import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean

class GroupCustomTheme(Base):
  id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
  descr: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
  active: Mapped[bool] = mapped_column(Boolean, default=True, unique=False, nullable=False)
  
  def __init__(self, descr: str):
    self.descr = descr