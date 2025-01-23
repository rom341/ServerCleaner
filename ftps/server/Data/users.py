from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from Data.table_base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, autoincrement=True)
    name = Column(String)
    files = relationship("File", back_populates="owner")

    def __init__(self, name, files):
        self.name = name
        self.files = files