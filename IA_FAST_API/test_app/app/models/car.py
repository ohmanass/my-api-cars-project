from app.db.base import Base
from sqlalchemy import Column, Integer, String

class Car(Base):    
    __tablename__ = "cars"
    
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    description = Column(String, nullable=True)