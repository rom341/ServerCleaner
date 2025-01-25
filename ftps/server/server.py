from ftps.Data.Repositories.db_connection import DBConnection
from ftps.Data.template import Template
from ftps.Data.user import User
from Data.ftps_server import FtpsServer


ftps_server = FtpsServer()
ftps_server.start_server()

# Create a new session
connection = DBConnection("sqlite:///mydb.db")
session = connection.create_new_session(echo=False)

# Check if the user already exists
user = session.query(User).filter_by(id=1).first()
if not user:
    user = User("Oleg", [])
    session.add(user)

# Check if the file already exists
file = session.query(Template).filter_by(id=1).first()
if not file:
    file = Template(
        owner=user,
        description="Test file",
        ttl_default=3600,
        keep_alive=True,
        keep_alive_timer=600,
        keep_alive_increment=300
    )
    session.add(file)

session.commit()

# Retrieving and printing the user and files
retrieved_user = session.query(User).first()
print(retrieved_user.name)
for f in retrieved_user.files:
    print(f.description) 


connection.close_session()
