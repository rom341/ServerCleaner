from ftps.Data.Repositories import db_connection
from ftps.Data.user import User
from sqlalchemy.orm import joinedload

class UserRepository:
    def __init__(self, db_connection):
        self.connection = db_connection 

    def create_user(self, user):
        session = self.connection.create_new_session()
        session.add(user)
        session.commit()
        session.close()

    def get_user_by_id(self, user_id):
        session = self.connection.create_new_session(echo=False)
        user = session.query(User).options(joinedload(User.templates)).filter_by(id=user_id).first() 
        session.close()
        return user

    def get_user_by_name(self, user_name):
        session = self.connection.create_new_session(echo=False)
        user = session.query(User).options(joinedload(User.templates)).filter_by(name=user_name).first() 
        session.close()
        return user

    def get_all_users(self):
        session = self.connection.create_new_session(echo=False)
        users = session.query(User).options(joinedload(User.templates)).all()
        session.close()
        return users

    def update_user(self, user_id, name):
        session = self.connection.create_new_session()
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            user.name = name 
            session.commit() 
        session.close()
        return user

    def delete_user(self, user_id):
        session = self.connection.create_new_session()
        user = session.query(User).filter_by(id=user_id).first() 
        if user:
            session.delete(user) 
            session.commit() 
        session.close() 
        return user
