from flask import json
from flask_restful import Resource
from marshmallow import Schema, fields
from webargs.flaskparser import use_args
from db import mongo
from util import mongo_id_decoder, validate_stock_id


class GetSchema(Schema):
    _id = fields.Function(deserialize=mongo_id_decoder)
    companyName = fields.Str()
    symbol = fields.Str()


class PostSchema(Schema):
    companyName = fields.Str(required=True)
    symbol = fields.Str(required=True)


class PutQuerySchema(Schema):
    _id = fields.Function(
        deserialize=mongo_id_decoder, validate=validate_stock_id, required=True
    )


class PutBodySchema(Schema):
    companyName = fields.Str(required=True)
    symbol = fields.Str(required=True)


class DeleteSchema(Schema):
    _id = fields.Function(
        deserialize=mongo_id_decoder, validate=validate_stock_id, required=True
    )


class Stock(Resource):
    @use_args(GetSchema(), location="querystring")
    def get(self, query):
        # Search for all stocks that match query arguments
        stocks = [stock for stock in mongo.db.stock.find(query)]
        return json.jsonify(data=stocks)

    @use_args(PostSchema(), location="json")
    def post(self, body):
        # Create stock with data from request
        mongo.db.stock.insert_one(body)
        return json.jsonify(data=body)

    @use_args(PutQuerySchema(), location="querystring")
    @use_args(PutBodySchema(), location="json")
    def put(self, query, body):
        stock_id = query.get("_id")
        # Update stock with data from request
        mongo.db.stock.update_one({"_id": stock_id}, {"$set": body})
        updated_stock = mongo.db.stock.find_one({"_id": stock_id})
        return json.jsonify(data=updated_stock)

    @use_args(DeleteSchema(), location="querystring")
    def delete(self, query):
        stock_id = query.get("_id")
        # Delete stock based on _id
        mongo.db.stock.delete_one({"_id": stock_id})
        return {"message": "Stock was deleted"}