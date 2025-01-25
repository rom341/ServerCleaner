from ftps.Data.client_server_path import ClientServerPath
from ftps.Data.Repositories.client_server_path_repository import ClientServerPathRepository
from ftps.Data.template import Template
from ftps.Data.Repositories import db_connection
from sqlalchemy.orm import joinedload

class TemplateRepository:
    def __init__(self, db_connection):
        self.connection = db_connection
        self.client_server_path_repo = ClientServerPathRepository(db_connection)

    def create_template(self, template):
        session = self.connection.create_new_session(echo=False)
        try:
            session.add(template)
            session.commit()
            self.client_server_path_repo.create_client_server_paths(template.id, template.client_server_paths)
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self.connection.close_session()

    def get_all_templates(self):
        session = self.connection.create_new_session(echo=False)
        try:
            return session.query(Template).options(
                joinedload(Template.client_server_paths),
                joinedload(Template.owner)
                ).all()
        finally:
            self.connection.close_session()

    def get_template_by_id(self, template_id):
        session = self.connection.create_new_session(echo=False)
        try:
            return session.query(Template).options(
                joinedload(Template.client_server_paths),
                joinedload(Template.owner)
                ).filter(Template.id == template_id).first()
        finally:
            self.connection.close_session()

    def update_template(self, template_id, updated_data):
        session = self.connection.create_new_session(echo=False)
        try:
            template = session.query(Template).filter(Template.id == template_id).first()
            if not template:
                return False

            for key, value in updated_data.items():
                setattr(template, key, value)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self.connection.close_session()

    def delete_template(self, template_id):
        session = self.connection.create_new_session(echo=False)
        try:
            template = session.query(Template).filter(Template.id == template_id).first()
            if not template:
                return False

            session.delete(template)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self.connection.close_session()

    def find_templates_by_owner(self, owner_id):
        session = self.connection.create_new_session(echo=False)
        try:
            return session.query(Template).options(
                joinedload(Template.client_server_paths),
                joinedload(Template.owner)
                ).filter(Template.owner_id == owner_id).all()
        finally:
            self.connection.close_session()
