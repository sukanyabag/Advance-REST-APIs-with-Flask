#this code is an internal representation of what an item looks like
#import sqlite3
from db import db

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    
    #notice referential integrity
    #store_id = foreign key of stores table that maps to primary key 'id' of items table
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))

    #one to many relationship - store containing n items
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "SELECT * FROM items WHERE name=?"
        #result = cursor.execute(query, (name,))
        #row = result.fetchone()
        #connection.close()

        #if row:
            #name = row[0], price = row[1]
            #*row -> (row[0], row[1]) - variable unpacking
            #return cls(*row)
        return cls.query.filter_by(name=name).first() #SELECT * FROM items where name= name LIMIT 1


    #does the job of insert as well as update
    def save_to_db(self):

        #session- collection of objs to be written to database
        db.session.add(self)
        db.session.commit()

    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()