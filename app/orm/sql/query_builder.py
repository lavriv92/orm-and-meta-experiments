from ..exceptions import InvalidQuery
from ..utils import get_keys, get_selection_keys, get_tablename
from .utils import normalize_conditions


class QueryBuilder:
    __tmp_query = None

    def __init__(self, model):
        self.model = model

    @property
    def __table_name(self):
        return get_tablename(self.model)

    @property
    def __formatted_keys(self):
        return ",".join(get_selection_keys(self.model))

    def __format_values(self, instance):
        values = [f"{v!r}" for v in vars(instance).values()]

        return ",".join(values)

    def create(self, instance):
        keys = ",".join(get_keys(instance.__class__))

        self.__tmp_query = f"INSERT INTO {self.__table_name}({keys}) VALUES({self.__format_values(instance)})"
        return self

    def build(self):
        return f"{self.__tmp_query};"

    def select(self, fields):
        self.__tmp_query = f"SELECT {self.__formatted_keys} FROM {self.__table_name}"
        return self

    def where(self, **conditions: dict):
        if self.__tmp_query is None:
            raise InvalidQuery("Tmp query shold be not start from where")

        formatted_conditions = normalize_conditions(conditions)
        self.__tmp_query += f" WHERE {formatted_conditions}"

        return self

    def skip(self, number):
        if self.__tmp_query is None:
            raise InvalidQuery("Tmp query shold be not start from where")

        self.__tmp_query += f" OFFSET {number}"

        return self

    def limit(self, limit):
        if self.__tmp_query is None:
            raise InvalidQuery("Tmp query is invalid")

        self.__tmp_query += f" LIMIT {limit}"

        return self

    def join(self, other_model):
        pass
