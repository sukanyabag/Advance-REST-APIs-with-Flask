#resources - external representation of an entity
#api clients -> mobile app/ website think that 
# they are interacting with resources, as api responds with resources.
#this code is an external representation of user entity

#import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


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




