from ftplib import FTP_TLS, error_perm
from Data.template import ClientServerPathPair
import os

class FtpsClient:    
    def __init__(self, server_address, login, password):
        self.server_addresss = server_address
        self.login = login
        self.passwod = password

    def check_files_exist(self, ftps, directory):
        try:
            file_list = ftps.nlst(directory)
            return set(file_list)
        except error_perm:
            return set() 

    def upload_files(self, ftps, source, destination):
        if os.path.isfile(source):
            with open(source, 'rb') as f:
                ftps.storbinary(f'STOR {destination}', f)
        else:
            ftps.mkd(destination)
            for filename in os.listdir(source):
                self.upload_files(ftps, os.path.join(source, filename), os.path.join(destination, filename))

    def send_files(self, path_pairs):
        ftps = FTP_TLS(self.server_addresss)
        ftps.login(self.login, self.server_addresss)
        ftps.prot_p()
        
        for pair in path_pairs:
            remote_files = self.check_files_exist(ftps, pair.destination)
            local_files = {os.path.join(pair.destination, f) for f in os.listdir(pair.source)}
            
            if remote_files & local_files:
                print(f"Files already exist on server for: {pair.destination}")
            else:
                self.upload_files(ftps, pair.source, pair.destination)
        
        ftps.quit()
