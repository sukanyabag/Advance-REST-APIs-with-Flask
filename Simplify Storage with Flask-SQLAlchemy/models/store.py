#this code is an internal representation of what an item looks like
#import sqlite3
from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    
    #allows a store to see what items are there in the items database
    #or in items table with a store_id = its own id.
    
    #many to 1 relationship - many items with 1 store_id
    
    # lazy = 'dynamic' querying with lazy = ‘dynamic’, however, generates 
    # a separate query for the related object and benefits you in querying 
    # further to return what you want. 
    items = db.relationship('ItemModel', lazy = 'dynamic')

    def __init__(self, name):
        self.name = name
        

    def json(self):
        #since we set lazy as dynamic, so to return the list of items, we need to call .all( )
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

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