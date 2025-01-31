from sqlalchemy import Column, Float, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"

    id = Column(String, primary_key=True, index=True)
    loc = Column(JSON)  # Store location as a JSON field
    userId = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    status = Column(String, index=True)
