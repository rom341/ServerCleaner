from ftps.Data.Models.client_server_path import ClientServerPath
from ftps.Data.Repositories import db_connection

class ClientServerPathRepository:
    def __init__(self, db_connection):
        self.connection = db_connection

    def create_client_server_paths(self, template_id, paths):
        session = self.connection.create_new_session(echo=False)
        try:
            for path in paths:
                client_server_path = ClientServerPath(
                    source=path.source,
                    destination=path.destination,
                    template_id=template_id
                )
                session.add(client_server_path)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self.connection.close_session()

    def get_all_paths_by_template_id(self, template_id):
        session = self.connection.create_new_session(echo=False)
        try:
            return session.query(ClientServerPath).filter(ClientServerPath.template_id == template_id).all()
        finally:
            self.connection.close_session()

    def delete_paths_by_template_id(self, template_id):
        session = self.connection.create_new_session(echo=False)
        try:
            session.query(ClientServerPath).filter(ClientServerPath.template_id == template_id).delete()
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self.connection.close_session()

    def update_client_server_path(self, path_id, updated_path):
        session = self.connection.create_new_session(echo=False)
        try:
            path = session.query(ClientServerPath).filter(ClientServerPath.id == path_id).first()
            if not path:
                return False

            path.source = updated_path.source
            path.destination = updated_path.destination
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            self.connection.close_session()
