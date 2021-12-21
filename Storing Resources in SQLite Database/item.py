import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

#crud api - create,read, update , delete
class Item(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('price',
            type = float,
            required = True,
            help = 'This field cannnot be left blank!')
    
    @jwt_required() #decorator, should be put in all methods for production apis
    #note - authenticate 1st in postman before calling get method
    #The GET method is used to access data for a specific resource from a REST API
    def get(self, name):
        #next - returns next item from the iterator
        #item = next(filter(lambda x: x['name'] == name, items), None)
        #return {'item' : item}, 200 if item else 404 #status code - 404 not found, 200 OK
        
        #retrieving data from database connected
        item = self.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not found!'}, 404
        if row:
            return {'item': { 'name': row[0],'price': row[1]}}
        

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}

                 
    #POST method is call when you have to add a child resource under resources collection
    def post(self, name):
        #if next(filter(lambda x: x['name'] == name, items), None) is not None:
            #return {'message': "An item with name '{}' already exists.".format(name)}, 400 #status code - 400 bad request
        if self.find_by_name(name):
            return {'message':"An item with name '{}' already exists.".format(name)}, 400        
        
        data = Item.parser.parse_args()
        #json payload, silent=True -> returns none, no error msg
        #data = request.get_json(silent=True)
        item = {'name': name, 'price':data['price']}

        try:
            self.insert(item)
        except:
            return {"message": "An error occured inserting the item."}, 500 #status code 500- Internal server error
        
        return item, 201 #status code - 201 created
        #items.append(item)
        #connection = sqlite3.connect('data.db')
        #cursor = connection.cursor()

        #query = "INSERT INTO items VALUES (?,?)"

        #cursor.execute(query, (item['name'], item['price']))
        
        #connection.commit()
        #connection.close()   
    
    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?,?)"

        cursor.execute(query, (item['name'], item['price']))
        
        connection.commit()
        connection.close()
  

    #The DELETE method requests that the origin server delete the resource identified by the Request-URI
    def delete(self, name):
        #global items #list of items
        #items = list(filter(lambda x: x['name'] != name, items))
        #return {'message' : 'Item has been successfully deleted!'}
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"

        cursor.execute(query, (name,))
        
        connection.commit()
        connection.close()

        return {'message':'Item has been deleted!'}
    #idempotent request - can call this rquest as many times needed, and o/p never changes
    #creates as well as updates an existing resource(items)
    
    #PUT method is call when you have to modify a single resource, which is already a part of resource collection
    def put(self, name):
        data = Item.parser.parse_args()
        
        #item = next(filter(lambda x: x['name'] == name, items), None)
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        
        #if no such item, create one
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message': "An error occured inserting the item!"}, 500

        #else, update existing item
        else:
            try:
                self.update(updated_item)
            except:
                return {'message': "An error occued updating the item!"}, 500
       
        return updated_item

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"

        cursor.execute(query, (item['price'],item['name']))
        
        connection.commit()
        connection.close()

        


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []

        for row in result:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {'items': items}
