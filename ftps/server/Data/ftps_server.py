from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

class FtpsServer:
    def __init__(self):
        self.authorizer = DummyAuthorizer()
        self.authorizer.add_user('user', '12345', '/', perm='elradfmw')
        self.authorizer.add_anonymous('/home/roman/ftps-test', perm='elradfmw')

    def start_server(self):
        handler = FTPHandler
        handler.authorizer = self.authorizer

        address = ('127.0.0.1', 2121)
        server = FTPServer(address, handler)

        print("FTP server started")
        server.serve_forever()
