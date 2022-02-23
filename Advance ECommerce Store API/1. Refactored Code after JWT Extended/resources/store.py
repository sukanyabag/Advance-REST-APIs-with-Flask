from flask_restful import Resource
from models.store import StoreModel

STORE_ALREADY_EXISTS = "'{}' store already exists!"
ERROR_CREATING_STORE = "An error occurred while creating the store '{}'."
STORE_NOT_FOUND = "'{}' store cannot be found! Please enter a valid store."
STORE_DELETED = "'{}' store has been successfully deleted!"


class Store(Resource):
  @classmethod
  def get(cls, name:str):
    store = StoreModel.find_store_by_name(name)
    if store:
      return store.json()
    return {"message" : STORE_NOT_FOUND.format(name)}, 404

  @classmethod
  def post(cls, name:str):
    if StoreModel.find_store_by_name(name):
      return {"message": STORE_ALREADY_EXISTS.format(name)}, 400

    store = StoreModel(name)

    try:
      store.save_to_database()
    except:
      return {"message": ERROR_CREATING_STORE.format(name)}, 500
        
    return store.json(), 201


  @classmethod
  def delete(cls, name:str):
    store = StoreModel.find_store_by_name(name)
    if store:
      store.delete_from_database()
      return {"message": STORE_DELETED.format(name)}

    return {"message": STORE_NOT_FOUND.format(name)}


class StoreList(Resource):
  @classmethod
  def get(cls):
    # return {"item": list(map(lambda x: x.json(), ItemModel.query.all()))}
    return {"stores": [store.json() for store in StoreModel.find_all()]}