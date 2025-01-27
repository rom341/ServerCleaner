from ftps.Data.Models.table_base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DBConnection:
    def __init__(self, db_connection_string): 
        self.db_connection_string = db_connection_string
        self.session={}

    def create_new_session(self, echo=False):
        engine = create_engine(self.db_connection_string, echo=echo)
        Base.metadata.create_all(bind=engine)

        Session = sessionmaker(bind=engine)
        self.session = Session()

        return self.get_session()

    def get_session(self):
        return self.session
    
    def close_session(self):
        self.session.close()