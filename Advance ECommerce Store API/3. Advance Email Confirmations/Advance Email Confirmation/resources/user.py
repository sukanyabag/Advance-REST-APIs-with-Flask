import traceback
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
from libs.mailgun import MailgunException
from libs.strings import get_text
from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST
from models.confirmation import ConfirmationModel


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
      return {"message": get_text("user_username_exists").format(user.username)}, 400

    if UserModel.find_by_email(user.email):
      # if exists, then don't add
      return {"message": get_text("user_email_exists")}, 400
    
    try:
      #save user to database
      user.save_to_database()
      #save confirmation details to the database before sending the confirmation email to the user
      confirmation = ConfirmationModel(user.id)
      confirmation.save_to_database()
      #now send confirmation email for account activation
      user.send_confirmation_email()
      return {"message": get_text("user_registered")}, 201

    #this block only happens when a problem is encountered while sending confirmation mail
    except MailgunException as e:
      user.delete_from_database()
      return {'message': str(e)}, 500

    #this block happens when the database fails/ database operational error 
    except:
      traceback.print_exc()
      user.delete_from_database()
      return {"message": get_text("user_error_creating")}, 500

 

class User(Resource):

  @classmethod
  def get(cls, user_id: int):

    user = UserModel.find_by_id(user_id)
    if not user:
      return {"message": get_text("user_not_found")}, 404
    
    #marshmallow dump method serializes app-level objs to primitive python types.
    #objs can then be rendered to standard json format for use in http-apis
    return user_schema.dump(user), 200
  
  @classmethod
  def delete(cls, user_id: int):
    user = UserModel.find_by_id(user_id)
    if not user:
      return {"message": get_text("user_not_found")}, 404

    user.delete_from_database()
    return {"message": get_text("user_deleted")}, 200


class UserLogin(Resource):
  @classmethod
  def post(cls):
    #fetch data from marshmallow schema.load()
    #partial means for logging in after account activation is done, email isn't required!
    user_data = user_schema.load(request.get_json(), partial=("email",))
    # find user in database
    user = UserModel.find_by_username(user_data.username)

    # check & compare password
    # this here is what authenticate() function used to do
    if user and safe_str_cmp(user.password, user_data.password):
      #vv imp to expire old confirmations if new one is requested
      confirmation = user.most_recent_confirmation
      if confirmation and confirmation.confirmed:
        # create access and refresh tokens
        access_token = create_access_token(identity=user.id, fresh=True)  # here, identity=user.id is what identity() used to do previously
        refresh_token = create_refresh_token(identity=user.id)
        print(get_text("user_logged_in"))
      
        return {
          "access_token": access_token,
          "refresh_token": refresh_token
        }, 200
      return {'message': get_text("user_not_confirmed").format(user.username)}, 400
         
    return {"message": get_text("user_invalid_credentials")}, 401 # Unauthorized


class UserLogout(Resource):
  # Logging out requires jwt as if user is not logged in they cannot log out
  @classmethod
  @jwt_required()
  def post(cls):
    jti = get_jwt()["jti"]   # jti is JWT ID, unique identifier for a JWT
    BLACKLIST.add(jti)
    return {"message":get_text("user_logged_out")}, 200

class TokenRefresh(Resource):
  @classmethod
  @jwt_required(refresh=True)
  def post(cls):
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user, fresh=False)   # fresh=Flase means that user have logged in days ago.

    return {"access_token": new_token}, 200



