from flask import request
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
  create_access_token, 
  create_refresh_token, 
  jwt_required, 
  get_jwt_identity,
  get_jwt
)
from marshmallow import ValidationError
from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST

USER_ALREADY_EXISTS = "An user with the name '{}' already exists!"
USER_CREATED = "User has been created successfully."
USER_NOT_FOUND = "User not found! Please enter a valid user."
USER_DELETED = "User with user_id '{}' has been deleted successfully!"
INVALID_CREDENTIALS = "The credentials entered are invalid! Please check again."
USER_LOGGED_IN = "User successfully logged in!"
USER_LOGGED_OUT = "User successfully logged out!"

# extracted parser variable for global use, and made it private
# _user_parser = reqparse.RequestParser()
# _user_parser.add_argument(
#   "username",
#   type=str,
#   required=True,
#   help= FIELD_BLANK_ERROR.format("username")
# )
# _user_parser.add_argument(
#   "password",
#   type=str,
#   required=True,
#   help=FIELD_BLANK_ERROR.format("password")
# ) 

#now reqparse will be replaced with marshmallow from here
user_schema = UserSchema()

# New user registration class
class UserRegister(Resource):
  # calls to post a new user (new user registration)
  @classmethod
  def post(cls):
    #reverse of dump
    #load will return a dict of field names mapped to deserialized values
    user = user_schema.load(request.get_json())
      
    # First check if that user is present or not
    if UserModel.find_by_username(user.username):
      # if exists, then don't add
      return {"message": USER_ALREADY_EXISTS.format(user.username)}, 400
    
    user.save_to_database()

    return {"messege": USER_CREATED}, 201
 

class User(Resource):

  @classmethod
  def get(cls, user_id: int):

    user = UserModel.find_by_id(user_id)
    if not user:
      return {"message": USER_NOT_FOUND}, 404
    
    #marshmallow dump method serializes app-level objs to primitive python types.
    #objs can then be rendered to standard json format for use in http-apis
    return user_schema.dump(user), 200
  
  @classmethod
  def delete(cls, user_id: int):
    user = UserModel.find_by_id(user_id)
    if not user:
      return {"message": USER_NOT_FOUND}, 404

    user.delete_from_database()
    return {"message": USER_DELETED.format(user_id)}, 200


class UserLogin(Resource):
  @classmethod
  def post(cls):
    #fetch data from marshmallow schema.load()
    user_data = user_schema.load(request.get_json())
    # find user in database
    user = UserModel.find_by_username(user_data.username)

    # check & compare password
    # this here is what authenticate() function used to do
    if user and safe_str_cmp(user.password, user_data.password):
      # create access and refresh tokens
      access_token = create_access_token(identity=user.id, fresh=True)  # here, identity=user.id is what identity() used to do previously
      refresh_token = create_refresh_token(identity=user.id)
      print(USER_LOGGED_IN)
      
      return {
        "access_token": access_token,
        "refresh_token": refresh_token
      }, 200
    
    return {"message": INVALID_CREDENTIALS}, 401 # Unauthorized


class UserLogout(Resource):
  # Logging out requires jwt as if user is not logged in they cannot log out
  @classmethod
  @jwt_required()
  def post(cls):
    jti = get_jwt()["jti"]   # jti is JWT ID, unique identifier for a JWT
    BLACKLIST.add(jti)
    return {"message":USER_LOGGED_OUT}, 200

class TokenRefresh(Resource):
  @classmethod
  @jwt_required(refresh=True)
  def post(cls):
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)   # fresh=Flase means that user have logged in days ago.

    return {"access_token": new_token}, 200