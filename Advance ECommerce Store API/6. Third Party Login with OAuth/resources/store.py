from flask import request
from flask_restful import Resource

from schemas.store import StoreSchema
from models.store import StoreModel

NAME_ALREADY_EXISTS = "Store alrady exists."
ERROR_INSERTING = "An error occured while creating the store."
STORE_NOT_FOUND = "Store not found."
STORE_DELETED = "Store deleted."


store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):
    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_store_by_name(name)
        if store:
            return store_schema.dump(store), 200

        return {"message": STORE_NOT_FOUND}, 404

    @classmethod
    def post(cls, name: str):
        if StoreModel.find_store_by_name(name):
            return {"message": NAME_ALREADY_EXISTS}, 400

        store = StoreModel(name=name)  # since __init__() method was removed from StoreModel, the name needs to be passed manually as such
        # as StoreModel is a model subclass, model class acceps keyword arguements and maps them to columns
        # so here, passing name as a keyword argument will map to name key in store model

        try:
            store.save_to_database()
        except:
            return {"message": ERROR_INSERTING}, 500

        return store_schema.dump(store), 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_store_by_name(name)
        if store:
            store.delete_from_database()
            return {"message": STORE_DELETED}

        return {"message": STORE_NOT_FOUND}


class StoreList(Resource):
    @classmethod
    def get(cls):
        # return {"item": list(map(lambda x: x.json(), ItemModel.query.all()))}
        return {"stores": [store_list_schema.dump(StoreModel.find_all())]}, 200
