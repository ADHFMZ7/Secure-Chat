from models import User

users = {}

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


# Change this when sessions are figured out.
def get_session(id: str) -> str | None:
    return None  
