from media_record.db import db_session
from media_record.models import *
def get_user(username, password):
    user = db_session.query(User).filter(User.username == username, User.password == password).first()

    if user:
        return user
    else:
        return None
    
def get_user_by_id(user_id):
    user =  db_session.query(User).filter(User.user_id == user_id).first()

    if user:
        return user
    else: 
        return None