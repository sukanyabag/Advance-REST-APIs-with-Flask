from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from db import db
from security import authenticate, identity
from resources.user import UserRegister, User
from resources.item import Item, ItemList 
from resources.store import Store, StoreList

app = Flask(__name__)
#connecting database (maybe postgre/sqlite/mysql etc)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
#sqlalchemy has its own built-in modif tracker to check if transactions committed are updated in the original database
#so disabling this feature can save memory on your server
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Exceptions are re-raised rather than being handled by the app’s error handlers.
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'chocobar'
api = Api(app)


#flask decorator to create tables automatically using sqlalchemy
@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000,debug=True)


   