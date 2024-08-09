from sqlalchemy.orm import Mapped, mapped_column
from .database import Base


class Urls(Base):
    __tablename__ = "urls"
    id: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    original_url: Mapped[str] = mapped_column("original_url", nullable=False)
    new_url: Mapped[str] = mapped_column("new_url", nullable=False)
