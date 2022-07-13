from xml.etree.ElementInclude import include
from ma import ma
from models.item import ItemModel
from models.store import StoreModel


class ItemSchema(ma.SQLAlchemyAutoSchema):
    # If the below Meta class is excluded, while fetching user information, we also fetch
    # the user password. So, password is included in the load_only tuple so that password field
    # is only loaded and not displayed.
    class Meta:
        model = ItemModel
        load_instance = True
        load_only = ("store",)  # makes 'store' field load_only. store_id will be displayed
        dump_only = ("id",)  # makes 'id' field dump_only.
        include_fk = True
