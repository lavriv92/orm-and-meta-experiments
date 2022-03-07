import sqlite3
from abc import ABC, abstractmethod
from contextlib import contextmanager

from .exceptions import RecordNotFound

from .sql.query_builder import QueryBuilder
from .utils import get_selection_keys, parse_connection_string


class BaseEngine(ABC):
    @abstractmethod
    def connect():
        pass

    @abstractmethod
    def close():
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def add(self, instance):
        pass

    @abstractmethod
    def select(self):
        pass


class SQlite3(BaseEngine):
    def __init__(self, uri: str):
        self.uri = uri

    def connect(self):
        self.connection = sqlite3.connect(self.uri)
        return self

    def commit(self):
        return self.connection.commit()

    def add(self, instance):
        query = QueryBuilder(instance.__class__).create(instance).build()
        res = self.connection.execute(query)

        setattr(instance, "id", res.lastrowid)

        return instance

    def get(self, model, id, fields=[]):
        query = QueryBuilder(model).select(fields).where(id=id).limit(1).build()
        item = self.connection.execute(query).fetchone()

        if item is None:
            raise RecordNotFound(f"{model.__name__} by {id!r} not found")

        keys = get_selection_keys(model)
        mapped_item = dict(zip(keys, item))

        return model(**mapped_item)

    def select(self, model, fields=[]):
        query = QueryBuilder(model).select(fields).build()
        results = self.connection.execute(query)
        keys = get_selection_keys(model)

        for row in results:
            mapped_item = dict(zip(keys, row))
            yield model(**mapped_item)

    def close(self):
        return self.connection.close()


ENGINES_MAP = {"sqlite3": SQlite3}


def create_database(connection_str):
    connection = parse_connection_string(connection_str)

    try:
        engine = ENGINES_MAP[connection["engine"]](connection["url"])
        return Database(engine=engine)
    except KeyError:
        print("Unsupported engine")


class Database:
    def __init__(self, engine: BaseEngine) -> None:
        self.engine = engine

    @contextmanager
    def connection(self) -> BaseEngine:
        try:
            yield self.engine.connect()
        finally:
            self.engine.close()
