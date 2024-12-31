from sqlalchemy import Column, Integer, PrimaryKeyConstraint, String,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


#TODO: composite key
class Clicks(Base):
    __tablename__ = "Clicks"

    id = Column(Integer, nullable=False,primary_key=True)  
    url_id = Column(Integer, ForeignKey("urls.id"), nullable=False)
    os = Column(String,nullable=False,server_default=text("unkown"))
    device = Column(String,nullable=False,server_default=text("unkown"))
    browser = Column(String,nullable=False,server_default=text("unkown"))
    client_ip = Column(String,nullable=True)
    timestamp = Column(
        TIMESTAMP(timezone=True), nullable=False, default=text("datetime()")
    )

    
    url = relationship("Urls", back_populates="clicks")