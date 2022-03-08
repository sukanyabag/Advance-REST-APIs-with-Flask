from xml.etree.ElementInclude import include
from ma import marshmallow_obj
from models.confirmation import ConfirmationModel

class ConfirmationSchema(marshmallow_obj.SQLAlchemyAutoSchema):
    class Meta:
        model = ConfirmationModel
        load_instance = True
        load_only = ("user",)
        dump_only = ("id", "expire_at", "confirmed")
        include_fk = True