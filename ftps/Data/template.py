from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ftps.Data.table_base import Base
from ftps.Data.client_server_path import ClientServerPath

class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="templates")
    description = Column(String)
    client_server_paths = relationship("ClientServerPath", backref="template", cascade="all, delete-orphan")
    ttlDefault = Column(Integer)  # Default time, that file can exist on server in seconds
    keepAlive = Column(Boolean)  # If true, it will expand ttl every {keepAliveTimer} seconds
    keepAliveTimer = Column(Integer)  # How often should client send 'keep alive increment'
    keepAliveIncrement = Column(Integer)  # If client is online, it will expand its ttl by this time in seconds

    def __init__(self, owner, description, paths, ttl_default, keep_alive, keep_alive_timer, keep_alive_increment):
        self.owner = owner
        self.description = description
        self.client_server_paths = paths
        self.ttlDefault = ttl_default
        self.keepAlive = keep_alive
        self.keepAliveTimer = keep_alive_timer
        self.keepAliveIncrement = keep_alive_increment
