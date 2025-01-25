from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from ftps.Data.table_base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    templates = relationship("Template", back_populates="owner")

    def __init__(self, name):
        self.name = name
