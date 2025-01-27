from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ftps.Data.Models.table_base import Base

class ClientServerPath(Base):
    __tablename__ = "client_server_paths"

    id = Column(Integer, primary_key=True, autoincrement=True)
    template_id = Column(Integer, ForeignKey("templates.id"), nullable=False)
    source = Column(String, nullable=False)
    destination = Column(String, nullable=False)

    def __init__(self, source, destination, template_id=None):
        self.source = source
        self.destination = destination
        self.template_id = template_id
