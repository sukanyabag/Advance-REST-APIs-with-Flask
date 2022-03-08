from flask_restful import Resource
from libs.strings import get_text
from models.store import StoreModel
from schemas.store import StoreSchema


store_schema = StoreSchema()
store_list_schemas = StoreSchema(many=True)


class Store(Resource):
  @classmethod
  def get(cls, name:str):
    store = StoreModel.find_store_by_name(name)
    if store:
      return store_schema.dump(store), 200
    return {"message" : get_text("store_not_found").format(name)}, 404

  @classmethod
  def post(cls, name:str):
    if StoreModel.find_store_by_name(name):
      return {"message": get_text("store_name_exists").format(name)}, 400

    store = StoreModel(name=name)

    try:
      store.save_to_database()
    except:
      return {"message": get_text("store_error_inserting").format(name)}, 500
        
    return store_schema.dump(store), 201


  @classmethod
  def delete(cls, name:str):
    store = StoreModel.find_store_by_name(name)
    if store:
      store.delete_from_database()
      return {"message": get_text("store_deleted").format(name)}

    return {"message": get_text("store_not_found").format(name)}


class StoreList(Resource):
  @classmethod
  def get(cls):
    # return {"item": list(map(lambda x: x.json(), ItemModel.query.all()))}
    return {"stores": store_list_schemas.dump(StoreModel.find_all())}, 200