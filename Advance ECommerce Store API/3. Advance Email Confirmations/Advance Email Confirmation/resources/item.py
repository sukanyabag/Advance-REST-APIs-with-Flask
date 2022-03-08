from flask import Flask, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from marshmallow import ValidationError
from schemas.item import ItemSchema
from models.item import ItemModel
from libs.strings import get_text


item_schema = ItemSchema()
#Set many=True when dealing with iterable collections of objects.
item_list_schema = ItemSchema(many=True)


class Item(Resource):
  # TO GET ITEM WITH NAME
  @classmethod
  @jwt_required()
  def get(cls, name: str):
    item = ItemModel.find_item_by_name(name)
    if item:
      return item_schema.dump(item), 200
    
    return {"message": get_text("item_not_found")}, 404

  # TO POST AN ITEM
  @classmethod
  @jwt_required(fresh=True)
  def post(cls, name: str):
    # if there already exists an item with "name", show a messege, and donot add the item
    if ItemModel.find_item_by_name(name):
      return {"message": get_text("item_name_exists").format(name)} ,400

    item_json = request.get_json()
    item_json["name"] = name
    # data = request.get_json()   # get_json(force=True) means, we don't need a content type header
    
    item = item_schema.load(item_json)

    try:

      item.save_to_database()

    except:

      return {"message": get_text("item_error_inserting")}, 500
    
    return item_schema.dump(item), 201   

  # TO DELETE AN ITEM
  @classmethod
  @jwt_required()
  def delete(cls, name: str):
    claims = get_jwt()

    if not claims["is_admin"]:
      return {"message": get_text("item_admin_priviledges_reqd")}, 401

    item = ItemModel.find_item_by_name(name)
    if item:
      item.delete_from_database()
      return {"message": get_text("item_deleted").format(name)}, 200

    # if doesn't exist, skip deleting 
    return {"message": get_text("item_not_found")}, 404

  # TO ADD OR UPDATE AN ITEM
  @classmethod
  def put(cls, name: str):
    item_json = request.get_json()
    item = ItemModel.find_item_by_name(name)

    # if item is not available, add it. Load it to the item schema
    if item is None:
      item_json["name"] = name
      item = item_schema.load(item_json)
    # if item exists, update it
    else:
      item.price = item_json["price"]
      item.store_id = item_json['store_id']
    
    # whether item is changed or inserted, it has to be saved to db
    item.save_to_database()
    # and dumped from the item schema to response user with the api
    return item_schema.dump(item), 200


class ItemList(Resource):
  @classmethod
  @jwt_required(optional=True)
  def get(cls):
    user_id = get_jwt_identity()
    items = item_list_schema.dump(ItemModel.find_all())

    # if user id is given, then display full details
    if user_id:
      return {"items": items}, 200

    # else display only item name
    return {
      "items": [item["name"] for item in items],
      "message": get_text("item_login_to_view_data")
    }, 200