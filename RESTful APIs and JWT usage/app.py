from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
app.secret_key = 'chocobar'
api = Api(app)

items = []

# restful api works with resources, and each resource must be a class
#resources are stored in databases
#restful api automatically jsonifies
#here - class Students inherits from the class Resource
class Item(Resource):
    def get(self, name):
        #next - returns next item from the iterator
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item' : item}, 200 if item else 404 #status code - 404 not found, 200 OK

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists.".format(name)}, 400 #status code - 400 bad request

        #json payload, silent=True -> returns none, no error msg
        data = request.get_json(silent=True)
        item = {'name': name, 'price':data['price']}
        items.append(item)
        return item, 201 #status code - 201 created

class ItemList(Resource):
    def get(self):
        return {'item' : items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000,debug=True)
   
