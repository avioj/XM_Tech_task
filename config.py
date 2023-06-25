import json
from pathlib import Path

from pydantic import BaseModel

from models.config_models.postgres_config import PostgresConfig


class ServerConfig(BaseModel):
    postgres: PostgresConfig


server_config_file = Path(__file__).parent / "server_config.json"
config = ServerConfig(**json.loads(server_config_file.read_text()))
