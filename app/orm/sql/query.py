from app.orm.utils import get_selection_keys
from .query_builder import QueryBuilder


class Query:
    def __init__(self, engine, model):
        self.model = model
        self.engine = engine
        self.query = QueryBuilder(model)

    def select(self, params):
        self.query = self.query.select(params)

    @property
    def __final_query(self):
        return self.query.build()

    def where(self, **conditions: dict):
        self.query = self.query.where(conditions)

    def all(self):
        results = self.engine.execute(self.__final_query).fetchall()
        keys = get_selection_keys(self.model)

        for item in results:
            normalized_item = dict(zip(keys, item))

            yield self.model(**normalized_item)
