#resources - external representation of an entity
#api clients -> mobile app/ website think that 
# they are interacting with resources, as api responds with resources.
#this code is an external representation of user entity

#import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
from blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )


class UserRegister(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with this username already exists."}, 400

        user = UserModel(**data) #unpacked kwargs
        user.save_to_db()

        return {'message': "User created successfully."}, 201 #201- is created
    
class User(Resource):
    """
    This resource can be useful when testing our Flask app
    when we are manipulating data regarding the users.
    """
    
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        return user.json(), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User Not Found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted.'}, 200

    
class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        # this is what the `authenticate()` function did in security.py
        if user and safe_str_cmp(user.password, data['password']):
            # identity= is what the identity() function did in security.py—now stored in the JWT
            access_token = create_access_token(identity=user.id, fresh=True) 
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {"message": "Invalid Credentials!"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']  # jti is "JWT ID", a unique identifier for a JWT.
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        """
        Get a new access token without requiring username and password—only the 'refresh token'
        provided in the /login endpoint.
        Note that refreshed access tokens have a `fresh=False`, which means that the user may have not
        given us their username and password for potentially a long time (if the token has been
        refreshed many times over).
        """
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200



