from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
import traceback
from flask import request


from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST
from libs.mailgun import MailgunException
from models.confirmation import ConfirmationModel

user_schema = UserSchema()

USER_ALREADY_EXISTS = "A user with that username already exists."
EMAIL_ALREADY_EXISTS = "A user with that email already exists."
USER_NOT_FOUND = "User not found."
USER_DELETED = "User deleted."
INVALID_CREDENTIALS = "Invalid credentials!"
USER_LOGGED_OUT = "User <id={user_id}> successfully logged out."
NOT_CONFIRMED_ERROR = "You have not confirmed registration, please check your email <{}>."
FAILED_TO_CREATE = "Internal server error. Failed to create user."
SUCCESS_REGISTER_MESSAGE = "Account created successfully, an email with an activation link has been sent to your email address, please check."


# New user registration class
class UserRegister(Resource):

    # calls to post a new user (new user registration)
    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())

        # First check if that user is present or not
        if UserModel.find_by_username(user.username):
            # if exists, then don't add
            return {"message": USER_ALREADY_EXISTS}, 400
        if UserModel.find_by_email(user.email):
            # if exists, then don't add
            return {"message": EMAIL_ALREADY_EXISTS}, 400

        # user = UserModel(data["username"], data["password"])
        # user = UserModel(**user_data)  # since parser only takes in username and password, only those two will be added.
        # flask_marshmallow already creates a user model, so we need not do it manually
        try:
            user.save_to_database()
            confirmation = ConfirmationModel(user.id)
            confirmation.save_to_database()
            user.send_confirmation_email()
            return {
                "messege": SUCCESS_REGISTER_MESSAGE,
            }, 201
        # Delete user from database in case of any Mailgun error
        except MailgunException as e:
            user.delete_from_database()
            return {"message", str(e)}, 500
        except:
            # print(err.messages)
            traceback.print_exc()
            user.delete_from_database()
            return {"message": FAILED_TO_CREATE}


class User(Resource):
    @classmethod
    def get(cls, user_id: int):

        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": USER_NOT_FOUND}, 404

        user.delete_from_database()
        return {"message": USER_DELETED}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from user to login. Include email to optional field.
        user_data = user_schema.load(request.get_json(), partial=("email",))

        # find user in database
        user = UserModel.find_by_username(user_data.username)

        # check password
        # this here is what authenticate() function used to do
        if user and safe_str_cmp(user.password, user_data.password):
            confirmation = user.most_recent_confirmation
            # print("user resource: ", confirmation.id)
            # Check if user is activated
            if confirmation and confirmation.confirmed:
                # create access and refresh tokens
                access_token = create_access_token(identity=user.id, fresh=True)  # here, identity=user.id is what identity() used to do previously
                refresh_token = create_refresh_token(identity=user.id)
                # print("user logged in")

                return {"access_token": access_token, "refresh_token": refresh_token}, 200
            # If user is not activated
            return {"message": NOT_CONFIRMED_ERROR}

        return {"message": INVALID_CREDENTIALS}, 401  # Unauthorized


class UserLogout(Resource):
    # Loggig out requirees jwt as if user is not logged in they cannot log out
    @classmethod
    @jwt_required()
    def post(cls):
        jti = get_jwt()["jti"]  # jti is JWT ID, unique identifier for a JWT
        BLACKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(jti)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_required(refresh=True)
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)  # fresh=Flase means that user have logged in days ago.

        return {"access_token": new_token}, 200
