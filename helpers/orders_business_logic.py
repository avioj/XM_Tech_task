from time import sleep

from clients.postgress.postgres_client import PostgresClient
from models.db_models.orders import Order, StatusEnum


def push_statuses(pg_client: PostgresClient, order_id):
    order = pg_client.get_first(Order, id=order_id)
    sleep(10)
    order.status = StatusEnum.executed
    pg_client.merge(order)
