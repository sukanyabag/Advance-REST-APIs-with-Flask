from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)

api = Api(app)

# restful api works with resources, and each resource must be a class

#here - class Students inherits from the class Resource
class Student(Resource):
    def get(self, name):
        return {'student' : name}

api.add_resource(Student, '/student/<string:name>')

app.run(debug=True)
