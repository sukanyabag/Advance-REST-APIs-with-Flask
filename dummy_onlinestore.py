from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        'name' : 'Online Shopping Store',
        'items' : [
            {
                'name' : 'My items',
                'price' : 20.78
            }
        ]
    }
]

@app.route('/')
def home():
    return render_template('index.html')

#for server - (flask sever)
#POST - used to receive data
#GET - used to send data back only

#for browser
#POST - used to send us data
#GET - used to receive data

#endpoints-
#POST /store data: {name:} - creates a new store with a given name
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json() #req made to endpoint
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

#GET  /store/<string:name> - get a store for a given name and return some data about it

@app.route('/store/<string:name>', methods=['GET'])
def get_store(name):
    #iterate over store
    # if store name matches return it
    #if not, return an error message
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message':'store not found!'})


    
#GET /store  - returns the list of all the stores
@app.route('/store', methods=['GET'])
def get_stores():
    return jsonify({'stores': stores})
    

#POST /store/<string:name>/item  data: {name:, price:} - creates an item in a specific store with a given name
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name' : request_data['name'],
                'price' : request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'message':'store not found!'})
    

#GET /store/<string:name>/item - gets all the item in a specific store
@app.route('/store/<string:name>/item', methods=['GET'])

def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items' : store['items']})
    return jsonify({'message':'store not found!'})

app.run(port=5000)








