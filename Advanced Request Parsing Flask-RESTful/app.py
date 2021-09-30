from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'chocobar'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

items = []

# restful api works with resources, and each resource must be a class
#resources are stored in databases
#restful api automatically jsonifies
#here - class Items inherits from the class Resource
class Item(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('price',
            type = float,
            required = True,
            help = 'This field cannnot be left blank!')
    @jwt_required() #decorator, should be put in all methods for production apis
    #note - authenticate 1st in postman before calling get method
    def get(self, name):
        #next - returns next item from the iterator
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item' : item}, 200 if item else 404 #status code - 404 not found, 200 OK

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400 #status code - 400 bad request
        
        data = Item.parser.parse_args()
        #json payload, silent=True -> returns none, no error msg
        #data = request.get_json(silent=True)
        item = {'name': name, 'price':data['price']}
        items.append(item)
        return item, 201 #status code - 201 created

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message' : 'Item has been successfully deleted.'}
    
    #idempotent request - can call this rquest as many times needed, and o/p never changes
    #creates as well as updates an existing resource(items)
    def put(self, name):
        data = Item.parser.parse_args()
        
        item = next(filter(lambda x: x['name'] == name, items), None)
        
        #if no such item, create one
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        #else, update existing item
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        return {'item' : items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000,debug=True)
   