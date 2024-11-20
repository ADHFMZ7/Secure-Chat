from models import User

users = {}

def get_user(username: str) -> User | None:
    if username in users:
        return users[username]

    return None

def register_user(username: str, password: str) -> str:
    
    new_user = User(username, password)
     
    users[new_user.username] = new_user 
    return new_user.username

# Change this when sessions are figured out.
def get_session(id: str) -> str | None:
    return None  
