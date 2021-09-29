from user import User
#compares strs and encodings -> returns true if strs/encodings are same
from werkzeug.security import safe_str_cmp
#in memory table of registered users
users = {
    User(1, 'Sukanya', bert)

}

username_mapping = {u.username: u for u in users} #set-comprehenion

userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)

    
