from ma import marshmallow_obj
#pre_dump->Reg a meth to invoke before dumping an obj. (runs before we dump a UserModel to json)
# The method receives the object to be serialized and returns the processed object.
from marshmallow import pre_dump 
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
        dump_only = ("id", "confirmation")

    @pre_dump(pass_many=True)
    #when we resend a confirmation, schema dump will not contain old/ expired confirmations
    def _pre_dump(self, user: UserModel, **kwargs):
        user.confirmation = [user.most_recent_confirmation]
        return user


    
