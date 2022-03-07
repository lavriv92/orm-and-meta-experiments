import sqlite3
from abc import ABC, abstractmethod
from contextlib import contextmanager

from .exceptions import RecordNotFound

from .query_builder import QueryBuilder
from .utils import get_keys, parse_connection_string


class BaseEngine(ABC):
    @abstractmethod
    def connect():
        pass

    @abstractmethod
    def close():
        pass

    # @abstractmethod
    # def execute(self, query):
    #     pass

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

    # def execute(self, query):
    #     results = self.database.execute(query)

    #     return {"results": results, "id": results.lastrowid}

    def commit(self):
        return self.connection.commit()

    def add(self, instance):
        query = QueryBuilder(instance.__class__).create(instance).build()
        res = self.connection.execute(query)

        setattr(instance, "id", res["id"])

        return instance

    def select(self, model):
        query = QueryBuilder(model).select().build()

        print("query", query)

        results = self.connection.execute(query)
        keys = get_keys(model)

        for row in results:
            yield model(**{k: v for k, v in zip(keys, row)})

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
