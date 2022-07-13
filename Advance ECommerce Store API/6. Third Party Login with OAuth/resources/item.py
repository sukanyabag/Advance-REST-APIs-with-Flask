from typing import Dict
from flask import request
from flask_restful import Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity,
)

from models.item import ItemModel
from schemas.item import ItemSchema

BLANK_ERROR = "'{}' cannot be blank"
ITEM_NOT_FOUND = "item not found."
NAME_ALREADY_EXISTS = "item '{}' already exists"
ERROR_INSERTING = "An error occured while inserting the item."
ITEM_DELETED = "Item deleted"

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):

    # TO GET ITEM WITH NAME
    @classmethod
    @jwt_required()
    def get(cls, name: str) -> Dict:
        item = ItemModel.find_item_by_name(name)
        if item:
            return item_schema.dump(item), 200

        return {"message": ITEM_NOT_FOUND}, 404

    # TO POST AN ITEM
    @classmethod
    @jwt_required(fresh=True)
    def post(cls, name: str):
        # if there already exists an item with "name", show a messege, and donot add the item
        if ItemModel.find_item_by_name(name):
            return {"messege": NAME_ALREADY_EXISTS.format(name)}, 400

        item_json = request.get_json()
        item_json["name"] = name  # this part is necessary to populate the payload with item name

        item = item_schema.load(item_json)

        # TODO: put these in above try except
        try:
            item.save_to_database()
        except:
            return {"messege": ERROR_INSERTING}, 500

        return item_schema.dump(item), 201  # 201 is for CREATED status

    # TO DELETE AN ITEM
    @classmethod
    @jwt_required()
    def delete(cls, name: str):
        claims = get_jwt()

        if not claims["is_admin"]:
            return {"message": "Admin privilages required"}, 401

        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_database()
            return {"messege": ITEM_DELETED}

        # if doesn't exist, skip deleting
        return {"messege": ITEM_NOT_FOUND}, 400

    # TO ADD OR UPDATE AN ITEM
    @classmethod
    def put(cls, name: str):
        item_json = request.get_json()

        item = ItemModel.find_item_by_name(name)

        # if item is not available, add it
        if item is None:
            item_json["name"] = name
            item = item_schema.load(item_json)

        # if item exists, update it
        else:
            item.price = item_json["price"]
            item.store_id = item_json["store_id"]

        # whether item is changed or inserted, it has to be saved to db
        item.save_to_database()
        return item_schema.dump(item), 200


class ItemList(Resource):
    @classmethod
    @jwt_required(optional=True)
    def get(cls):
        user_id = get_jwt_identity()
        items = [item_list_schema.dump(ItemModel.find_all())]

        # if user id is given, then display full details
        if user_id:
            return {"items": items}, 200

        # else display only item name
        return {
            "items": [item["name"] for item in items],
            "message": "Login to view more data.",
        }, 200
