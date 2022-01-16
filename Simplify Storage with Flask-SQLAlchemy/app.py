from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList 
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#sqlalchemy has its own built-in modif tracker to check if transactions committed are updated in the original database
#so disabling this feature can save memory on your server
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chocobar'
api = Api(app)


#flask decorator to create tables automatically using sqlalchemy
@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    #circular import
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)


   