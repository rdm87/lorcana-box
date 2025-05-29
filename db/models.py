from sqlalchemy import Column, Float, String, Integer
from db.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    box = Column(Integer, nullable=False)
    payd = Column(Float)
    topay = Column(Float)
    total = Column(Float)

class Spese(Base):
    __tablename__ = 'spese'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    costo = Column(Float)
