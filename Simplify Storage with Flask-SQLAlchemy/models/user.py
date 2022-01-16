#model - internal representation of an entity

import sqlite3
from db import db

#usermodel apis - find_by_username,find_by_id
class UserModel(db.Model): 
    __tablename__ = 'users'
    
    #id automtically increments
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        #self.id = _id
        self.username = username
        self.password = password
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def find_by_username(cls, username):
        
        return cls.query.filter_by(username=username).first()


    @classmethod
    def find_by_id(cls, _id):

        return cls.query.filter_by(id = _id).first()