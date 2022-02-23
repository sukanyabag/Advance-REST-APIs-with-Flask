from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
  create_access_token, 
  create_refresh_token, 
  jwt_required, 
  get_jwt_identity,
  get_jwt
)
from models.user import UserModel
from blacklist import BLACKLIST

# extracted parser variable for global use, and made it private
_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
  "username",
  type=str,
  required=True,
  help="This field cannot be empty"
)
_user_parser.add_argument(
  "password",
  type=str,
  required=True,
  help="This field cannot be empty"
)

# New user registraction class
class UserRegister(Resource):

  # calls to post a new user (new user registration)
  def post(self):
    data = _user_parser.parse_args()
    # First check if that user is present or not
    if UserModel.find_by_username(data["username"]):
      # if exists, then don't add
      return {"message": "An user with that username already exists."}, 400
    
    # user = UserModel(data["username"], data["password"])
    user = UserModel(**data)  # since parser only takes in username and password, only those two will be added.
    user.save_to_database()

    return {"messege": "User added successfully."}, 201


class User(Resource):

  @classmethod
  def get(cls, user_id: int):

    user = UserModel.find_by_id(user_id)
    if not user:
      return {"message": "User not found."}, 404
  
    return user.json(), 200
  
  @classmethod
  def delete(cls, user_id: int):
    user = UserModel.find_by_id(user_id)
    if not user:
      return {"message": "User not found."}, 404

    user.delete_from_database()
    return {"message": "User deleted."}, 200


class UserLogin(Resource):

  @classmethod
  def post(cls):
    # get data from parser
    data = _user_parser.parse_args()

    # find user in database
    user = UserModel.find_by_username(data["username"])

    # check password
    # this here is what authenticate() function used to do
    if user and safe_str_cmp(user.password, data["password"]):

      # create access and refresh tokens
      access_token = create_access_token(identity=user.id, fresh=True)  # here, identity=user.id is what identity() used to do previously
      refresh_token = create_refresh_token(identity=user.id)
      print("user logged in")
      
      return {
        "access_token": access_token,
        "refresh_token": refresh_token
      }, 200
    
    return {"message": "Invalid credentials."}, 401 # Unauthorized


class UserLogout(Resource):
  # Loggig out requirees jwt as if user is not logged in they cannot log out
  @jwt_required()
  def post(self):
    jti = get_jwt()["jti"]   # jti is JWT ID, unique identifier for a JWT
    BLACKLIST.add(jti)
    return {"message": "Successfully logged out."}, 200

class TokenRefresh(Resource):
  @jwt_required(refresh=True)
  def post(self):
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)   # fresh=Flase means that user have logged in days ago.

    return {"access_token": new_token}, 200