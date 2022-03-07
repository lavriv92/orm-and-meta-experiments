from concurrent.futures import thread
import sqlite3
from abc import ABC, abstractmethod

from .query_builder import QueryBuilder
from .utils import get_keys, parse_connection_string


class Engine(ABC):
    @abstractmethod
    def execute(self, query):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def close(self):
        pass


class SQlite3(Engine):
    def __init__(self, database):
        self.database = sqlite3.connect(database)

    def execute(self, query):
        results = self.database.execute(query)

        return {"results": results, "id": results.lastrowid}

    def commit(self):
        return self.database.commit()

    def close(self):
        return self.database.close()


ENGINES_MAP = {"sqlite3": SQlite3}


def create_database(connection_str):
    connection = parse_connection_string(connection_str)

    try:
        engine = ENGINES_MAP[connection["engine"]](connection["url"])
        return Session(engine=engine)
    except KeyError:
        print("Unsupported engine")


class Session:
    def __init__(self, engine: Engine = None):
        self.engine = engine

    def add(self, instance):
        query = QueryBuilder(instance.__class__).create(instance).build()
        res = self.engine.execute(query)

        setattr(instance, "id", res["id"])

    def select(self, model):
        query = QueryBuilder(model).select().build()

        results = self.engine.execute(query)

        keys = get_keys(model)

        return [
            model(**{k: v for k, v in zip(keys, row)}) for row in results["results"]
        ]

    def commit(self):
        self.engine.commit()

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        self.engine.close()
