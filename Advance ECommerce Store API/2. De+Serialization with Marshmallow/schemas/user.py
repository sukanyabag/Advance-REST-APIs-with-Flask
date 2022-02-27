from ma import marshmallow_obj
from models.user import UserModel

class UserSchema(marshmallow_obj.SQLAlchemyAutoSchema):
    #class meta is used to add security to the api get request, so it does not send
    #confidential info like password when dumping data
    class Meta:
        model = UserModel
        load_instance = True
        #says marshmallow that field password is only for loading(deserializing, here = for registering new user)
        # data,not dumping(serializing, here- responding an user by his/her id).
        load_only = ("password",)
        #id field is only needed to get user data like (get){{url}}/user/<id> (dumping/serializing)
        # using it to post data to a resource(deserializing/loading/creating from schema) is not necessary
        dump_only = ("id",)

    
