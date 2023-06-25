from pydantic import BaseModel


class PostgresConfig(BaseModel):
    user: str
    password: str
    host: str
    port: str
    database: str
