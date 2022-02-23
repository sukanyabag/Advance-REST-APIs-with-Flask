from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin,UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST
from database import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/data.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False    # turns of flask_sqlalchemy modification tracker
app.config["PROPAGATE_EXCEPTIONS"] = True   # if flask_jwt raises an error, the flask app will check the error if this is set to true
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]   # both access and refresh tokens will be denied for the user ids 

app.secret_key = "komraishumtirkomchuri"
# app.config["JWT_SECRET_KEY"] = "YOUR KEY HERE"

api = Api(app)

@app.before_first_request
def create_tables():
  db.create_all()
  # above function creates all the tables before the 1st request is made
  # unless they exist alraedy

# JWT() creates a new endpoint: /auth
# we send an username and password to /auth
# JWT() gets the username and password, and sends it to authenticate function
# the authenticate function maps the username and checks the password
# if all goes well, the authenticate function returns user
# which is the identity or jwt(or token)
# jwt = JWT(app, authenticate, identity)
jwt = JWTManager(app)   # JwtManager links up to the application, doesn't create /auth point

@jwt.additional_claims_loader   # modifies the below function, and links it with JWTManager, which in turn is linked with our app
def add_claims_to_jwt(identity):
  if identity == 1:   # insted of hardcoding this, we should read it from a config file or database
    return {"is_admin": True}
  
  return {"is_admin": False}

# JWT Configurations
@jwt.expired_token_loader
def expired_token_callback():
  return jsonify({
    "description": "The token has expired.",
    "error": "token_expired"
  }), 401

# below function returns True, if the token that is sent is in the blacklist
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_data):
  # print("Log Message:", jwt_data)
  return jwt_data["jti"] in BLACKLIST

@jwt.invalid_token_loader
def invalid_token_callback(error):
  return jsonify({
    "description": "Signature verification failed.",
    "error": "invalid_token"
  }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):  # when no jwt is sent
  return jsonify({
    "description": "Request doesn't contain a access token.",
    "error": "authorization_required"
  }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(self, callback):
  # print("Log:", callback)
  return jsonify({
    "description": "The token is not fresh.",
    "error": "fresh_token_required"
  }), 401

@jwt.revoked_token_loader
def revoked_token_callback(self, callback):
  # print("Log:", callback)
  return jsonify({
    "description": "The token has been revoked.",
    "error": "token_revoked"
  }), 401

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')

if __name__ == "__main__":
  db.init_app(app)
  app.run(port=5000, debug=True)