from ma import ma
from marshmallow import pre_dump
from models.user import UserModel


# use SQLAlchemyAutoSchema. ModelSchema is deprecated
class UserSchema(ma.SQLAlchemyAutoSchema):
    # If the below Meta class is excluded, while fetching user information, we also fetch
    # the user password. So, password is included in the load_only tuple so that password field
    # is only loaded and not displayed.
    class Meta:
        model = UserModel
        load_instance = True
        load_only = ("password",)  # makes 'password' field load_only
        dump_only = (
            "id",
            "confirmation",
        )  # makes 'id' field dump_only.

    @pre_dump
    def _pre_dump(self, user: UserModel, **kwargs):  # Here user is the user that will be turned to json
        user.confirmation = [user.most_recent_confirmation]
        return user
