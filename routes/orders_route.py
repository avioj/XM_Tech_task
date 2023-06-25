import uuid
from threading import Thread

from flask import Blueprint
from marshmallow import fields
from webargs.flaskparser import use_args

from clients.postgress.errors import DataBaseQueryIsEmpty
from clients.postgress.helpers import object_as_dict
from helpers.orders_business_logic import push_statuses
from models.db_models.orders import StatusEnum, Order
from . import pg_client

orders_blueprint = Blueprint('orders', __name__, url_prefix='/orders')


@orders_blueprint.route("", methods=["GET"])
def get_orders():
    return [*map(object_as_dict, pg_client.get_all(Order))], 200


@orders_blueprint.route("/<order_id>", methods=["GET"])
def get_order(order_id: str):
    return object_as_dict(pg_client.get_first(Order, id=order_id)), 200


@orders_blueprint.route("", methods=["POST"])
@use_args({"stocks": fields.Str(required=True), "quantity": fields.Int(required=True)}, location="json")
def create_order(body):
    order_id = pg_client.insert(Order(quantity=body["quantity"], stocks=body["stocks"],
                                      status=StatusEnum.pending))["id"]
    Thread(target=push_statuses, args=(pg_client, order_id)).start()
    return dict(id=order_id), 201


@orders_blueprint.route("/<order_id>", methods=["DELETE"])
def delete_order(order_id: str):
    pg_client.delete_one(Order, id=order_id)
    return "", 204
