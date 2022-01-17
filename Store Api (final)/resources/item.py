#this code is an external representation of entity item
#import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity, jwt_optional, fresh_jwt_required
from models.item import ItemModel
#crud api - create,read, update , delete


class Item(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('price',
            type = float,
            required = True,
            help = 'This field cannnot be left blank!')

    parser.add_argument('store_id',
            type = int,
            required = True,
            help = 'Every item needs a store id!')

    
    @jwt_required # No longer needs brackets
    #decorator, should be put in all methods for production apis
    #note - authenticate 1st in postman before calling get method
    #The GET method is used to access data for a specific resource from a REST API
    def get(self, name):
        #next - returns next item from the iterator
        #item = next(filter(lambda x: x['name'] == name, items), None)
        #return {'item' : item}, 200 if item else 404 #status code - 404 not found, 200 OK
        
        #retrieving data from database connected
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found!'}, 404
    
                     
    #POST method is call when you have to add a child resource under resources collection
    @fresh_jwt_required
    def post(self, name):
        #if next(filter(lambda x: x['name'] == name, items), None) is not None:
            #return {'message': "An item with name '{}' already exists.".format(name)}, 400 #status code - 400 bad request
        if ItemModel.find_by_name(name):
            return {'message':"An item with name '{}' already exists.".format(name)}, 400        
        
        data = Item.parser.parse_args()
        #json payload, silent=True -> returns none, no error msg
        #data = request.get_json(silent=True)

        #item = {'name': name, 'price':data['price']}
        #item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)


        try:
            item.save_to_db()
        except:
            return {"message": "An error occured while inserting the item."}, 500 #status code 500- Internal server error
        
        return item.json(), 201 #status code - 201 created
    
    
  

    #The DELETE method requests that the origin server delete the resource identified by the Request-URI
    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        
        item = ItemModel.find_by_name(name)
        
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}
        return {'message': 'Item not found.'}, 404
        
    
    
    #idempotent request - can call this rquest as many times needed, and o/p never changes
    #creates as well as updates an existing resource(items)
    #PUT method is call when you have to modify a single resource, which is already a part of resource collection
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json()

        
class ItemList(Resource):
    @jwt_optional
    def get(self):
        """
        Here we get the JWT identity, and then if the user is logged in (we were able to get an identity)
        we return the entire item list.
        Otherwise we just return the item names.
        This could be done with e.g. see orders that have been placed, but not see details about the orders
        unless the user has logged in.
        """
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {
            'items': [item['name'] for item in items],
            'message': 'More data available if you log in.'
        }, 200
