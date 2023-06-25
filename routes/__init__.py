from clients.postgress.postgres_client import PostgresClient
from config import config

pg_client = PostgresClient(config.postgres)
