from ftplib import FTP, error_perm
import os

class ClientServerPathPair:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination

class FTPClient:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ftp = None

    def connect(self):
        try:
            self.ftp = FTP()
            self.ftp.set_pasv(True)
            self.ftp.connect(host=self.host, port=int(self.port), timeout=30)
            self.ftp.login(self.username, self.password)
            print(f"Подключение к серверу {self.host}:{self.port} установлено.")
        except Exception as e:
            print(f"Ошибка при подключении к серверу: {e}")

    def disconnect(self):
        if self.ftp:
            self.ftp.quit()
            print("Соединение с сервером закрыто.")

    def is_directory_on_server(self, destination):
        try:
            self.ftp.cwd(destination)
            return True
        except Exception:
            return False
    
    def is_file_on_server(self, destination):
        try:
            self.ftp.voidcmd('TYPE I')
            self.ftp.cwd('/')
            self.ftp.size(destination)#if file is exists, function will return it size
            return True
        except Exception as e:
            print(e)
            return False

    def find_exist_files_on_server(self, path_pairs):     
        self.connect()
        existing_files = []
        for pair in path_pairs: 
            if(self.is_directory_on_server(pair.destination) or self.is_file_on_server(pair.destination)):
                existing_files.append(pair.destination)
        self.disconnect()
        return existing_files

    def send_file(self, local_file, remote_file):
        with open(local_file, "rb") as f:
            return self.ftp.storbinary(f"STOR {remote_file}", f)

    def upload_files(self, path_pairs):
        self.connect()
        try:
            for pair in path_pairs:
                if os.path.isdir(pair.source) and os.path.isfile(pair.destination):
                    print(f"Ошибка: Невозможно загрузить папку {pair.source} в файл {pair.destination}.")
                    return

                if os.path.isfile(pair.source):
                    if os.path.isdir(pair.destination):
                        destination_path = os.path.join(pair.destination, os.path.basename(pair.source)).replace("\\", "/")
                    else:
                        destination_path = pair.destination.replace("\\", "/")

                    self.send_file(pair.source, pair.destination)
                    #with open(pair.source, "rb") as f:
                    #    self.ftp.storbinary(f"STOR {os.path.basename(destination_path)}", f)
                    print(f"File {pair.source} uploaded to {destination_path}.")

                elif os.path.isdir(pair.source):
                    for root, _, files in os.walk(pair.source):
                        relative_path = os.path.relpath(root, pair.source)
                        remote_path = os.path.join(pair.destination, relative_path).replace("\\", "/")
                        try:
                            self.ftp.cwd(remote_path)
                        except Exception:
                            self.ftp.mkd(remote_path)

                        for file in files:
                            local_file = os.path.join(root, file)
                            remote_file = os.path.join(remote_path, file).replace("\\", "/")
                            self.send_file(local_file, remote_file)
                            #with open(local_file, "rb") as f:
                            #    self.ftp.storbinary(f"STOR {os.path.basename(remote_file)}", f)
                            print(f"File {local_file} uploaded to {remote_file}.")
        except Exception as e:
            print(f"Error while uploading file: {e}")
        finally:
            self.disconnect()
