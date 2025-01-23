from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from Data.table_base import Base


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key = True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="files")
    description = Column(String)
    ttl_default = Column(Integer)
    keep_alive = Column(Boolean)
    keep_alive_timer = Column(Integer)
    keep_alive_increment = Column(Integer)

    def __init__(self, owner, description, ttl_default, keep_alive, keep_alive_timer, keep_alive_increment):
        self.owner = owner
        self.description = description
        self.ttl_default = ttl_default
        self.keep_alive = keep_alive
        self.keep_alive_timer = keep_alive_timer
        self.keep_alive_increment = keep_alive_increment