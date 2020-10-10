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
    # Convert str to Mongo Object ID
    return ObjectId(obj)


def validate_user_id(user_id):
    user = mongo.db.user.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise ValidationError("Invalid User Id", "_id")


def validate_stock_id(stock_id):
    stock = mongo.db.stock.find_one({"_id": ObjectId(stock_id)})
    if not stock:
        raise ValidationError("Invalid Stock Id", "favoriteStockId")
