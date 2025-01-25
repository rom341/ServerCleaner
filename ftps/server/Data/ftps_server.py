from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler, TLS_FTPHandler
from pyftpdlib.servers import FTPServer

class FtpsServer:
    def __init__(self):
        self.authorizer = DummyAuthorizer()
        self.authorizer.add_user('user', '12345', '/home/roman/ftps-test', perm='elradfmw')
        self.authorizer.add_anonymous('/home/roman/ftps-test', perm='elradfmw')

    def start_server(self):        
        handler = TLS_FTPHandler
        handler.certfile = '/home/roman/code_tests/python/ServerCleaner/ftps/server/Config/ftps_cert.pem'
        handler.keyfile = '/home/roman/code_tests/python/ServerCleaner/ftps/server/Config/frps_key.pem'
        handler.authorizer = self.authorizer

        handler.tls_control_required = True
        handler.tls_data_required = True
        
        address = ('127.0.0.1', 2121)
        server = FTPServer(address, handler)
        
        server.serve_forever()
