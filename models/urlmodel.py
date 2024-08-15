from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class Urls(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, nullable=False)
    original_url = Column(String, unique=True, nullable=False)
    new_url = Column(String, unique=True, nullable=False)
    craeted_at = Column(
        TIMESTAMP(timezone=True), nullable=False, default=text("datetime()")
    )
    clicks = Column(Integer, nullable=False, server_default=text("0"))
