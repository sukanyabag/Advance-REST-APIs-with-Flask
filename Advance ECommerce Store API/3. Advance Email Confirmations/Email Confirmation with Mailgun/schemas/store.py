from ma import marshmallow_obj
from models.store import StoreModel
from models.item import ItemModel
from schemas.item import ItemSchema

class StoreSchema(marshmallow_obj.SQLAlchemyAutoSchema):
    #tells marshmallow that items property in store is nested inside
    #the store and contains many item schemas, hence it is not to be loaded but dumped
    items = marshmallow_obj.Nested(ItemSchema, many=True)
    
    
    class Meta:
        model = StoreModel
        load_instance = True
        dump_only = ("id",)
        include_fk = True
    