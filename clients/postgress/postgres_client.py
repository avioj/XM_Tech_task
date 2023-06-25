import contextlib
from typing import TypeVar, List, Dict

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

from clients.postgress.errors import PostgresClientError, DataBaseQueryIsEmpty
from clients.postgress.helpers import object_as_dict
from models.config_models.postgres_config import PostgresConfig
from models.db_models import Base

TABLE = TypeVar("TABLE", bound=Base)


class PostgresClient:

    def __init__(self, config: PostgresConfig):
        self._config = config
        self.db_engine = create_engine(f"postgresql://{self._config.user}:{self._config.password}@"
                                       f"{self._config.host}:{self._config.port}/"
                                       f"{self._config.database}")
        self.session = sessionmaker(bind=self.db_engine)

    @contextlib.contextmanager
    def err_handler(self):
        with self.session() as dbsession:
            try:
                yield dbsession
            except OperationalError as ex:
                dbsession.rollback()
                raise PostgresClientError(ex.args)

    def delete_one(self, table, **kwargs):
        with self.err_handler() as db_session:
            data = db_session.query(table).filter_by(**kwargs)
            if not data.first():
                raise DataBaseQueryIsEmpty(str(table), str(kwargs))
            data.delete()
            db_session.commit()

    def get_all(self, table: TABLE) -> List[TABLE]:
        with self.err_handler() as db_session:
            return db_session.query(table).all()

    def get_first(self, table: TABLE, **kwargs):
        with self.err_handler() as db_session:
            item = db_session.query(table).filter_by(**kwargs).first()
            if item is None:
                raise DataBaseQueryIsEmpty(str(table), str(kwargs))
            return item

    def insert(self, item) -> Dict:
        with self.err_handler() as db_session:
            db_session.add(item)
            db_session.commit()
            _dict = object_as_dict(item)
        return _dict

    def merge(self, item):
        with self.err_handler() as db_session:
            db_session.merge(item)
            db_session.commit()
