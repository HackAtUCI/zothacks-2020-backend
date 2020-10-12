import json
from marshmallow import ValidationError
from bson.objectid import ObjectId
from db import mongo


class MongoEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def mongo_id_decoder(obj):
    # Try to convert str to Mongo Object ID
    try:
        return ObjectId(obj)
    except Exception:
        raise ValidationError("Invalid User Id Format", "_id")


def validate_user_id(user_id):
    user = mongo.db.user.find_one({"_id": user_id})
    if not user:
        raise ValidationError("Invalid User Id", "_id")


def validate_stock_id(stock_id, field_name="_id"):
    stock = mongo.db.stock.find_one({"_id": stock_id})
    if not stock:
        raise ValidationError("Invalid Stock Id", field_name)


def validate_user_stock_id(stock_id):
    validate_stock_id(stock_id, field_name="favoriteStockId")
