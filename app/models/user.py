from .database import Base
from sqlalchemy import Integer, String, Column

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=False, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    