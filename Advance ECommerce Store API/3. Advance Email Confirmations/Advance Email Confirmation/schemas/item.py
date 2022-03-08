from ma import marshmallow_obj
from models.item import ItemModel
from models.store import StoreModel


class ItemSchema(marshmallow_obj.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_instance = True
        load_only = ("store",)
        dump_only = ("id",)
        # includes the foreign key 'store_id' during json dumps
        #for referential integrity(linking accross database tables)
        include_fk = True

