from models import User
from random import randint

users = {}
sessions = {}

def get_user(username: str) -> User | None:
    if username in users:
        return users[username]

    return None

def create_user(username: str, password: str) -> User | None:
  
    # Make sure username doesnt already exist
    if username in users:
        return None

    # Create user
    new_user = User(username, password)
    users[new_user.username] = new_user 

    # Return new user
    return new_user

def create_session(user: User):

    # Generate random key
    key = randint(int(1e50), int(1e100))

    # Store session information in map
    # Session should store:
    # user that is logged in
    # When logged in ??
    # When it expires??

    sessions[key] = user.username



# Change this when sessions are figured out.
def get_session(sesh_key: str) -> str | None:

    if sesh_key in sessions:
        return sessions[sesh_key]
    return None  
