import sqlite3
from flask_restful import Resource, reqparse

class User: 
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password
    
    #retrieves usr objects from the database
    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        
        #cursor.execute(<query_var>, <params>)
        # <params> should always be a tuple
        res = cursor.execute(query, (username,))
        row = res.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        
        #cursor.execute(<query_var>, <params>)
        # <params> should always be a tuple
        res = cursor.execute(query, (_id,))
        row = res.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
    type = str,
    required = True,
    help = "This field cannot be blank."
    )

    parser.add_argument('password',
    type = str,
    required = True,
    help = "This field cannot be blank."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "A user with this username already exists."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL, ?,?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit() 
        connection.close()

        return {'message': "User created successfully."}, 201 #201- is created




