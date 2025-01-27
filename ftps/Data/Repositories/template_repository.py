from ftps.Data.Models.client_server_path import ClientServerPath
from ftps.Data.Repositories.client_server_path_repository import ClientServerPathRepository
from ftps.Data.Models.template import Template
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
                joinedload(Template.clientServerPaths),
                joinedload(Template.owner)
                ).all()
        finally:
            self.connection.close_session()

    def get_template_by_id(self, template_id):
        session = self.connection.create_new_session(echo=False)
        try:
            return session.query(Template).options(
                joinedload(Template.clientServerPaths),
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

            current_paths = {path.id: path for path in template.clientServerPaths}
            updated_paths = {path.id: path for path in updated_data['paths'] if path.id is not None}

            # Remove paths that are not in updated paths
            for path_id, path in current_paths.items():
                if path_id not in updated_paths:
                    session.delete(path)
                
            # Add or update remaining paths
            for path in updated_data['paths']:
                if path.id is None:
                    path.template_id = template.id
                    session.add(path)
                else:
                    existing_path = current_paths.get(path.id)
                    existing_path.source = path.source
                    existing_path.destination = path.destination

            for key, value in updated_data.items():
                if key != "paths":
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
                joinedload(Template.clientServerPaths),
                joinedload(Template.owner)
                ).filter(Template.owner_id == owner_id).all()
        finally:
            self.connection.close_session()
