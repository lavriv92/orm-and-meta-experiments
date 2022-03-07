from .exceptions import InvalidQuery
from .utils import get_tablename


class QueryBuilder:
    __tmp_query = None

    def __init__(self, model):
        self.model = model

    @property
    def __table_name(self):
        return get_tablename(self.model)

    @property
    def __formatted_keys(self):
        keys = vars(self.model).get("__annotations__").keys()
        return ",".join(keys)

    def __format_values(self, instance):
        values = [f"{v!r}" for v in vars(instance).values()]

        return ",".join(values)

    def create(self, instance):
        self.__tmp_query = f"INSERT INTO {self.__table_name}({self.__formatted_keys}) VALUES({self.__format_values(instance)})"
        return self

    def build(self):
        return f"{self.__tmp_query};"

    def select(self):
        self.__tmp_query = f"SELECT id,{self.__formatted_keys} FROM {self.__table_name}"
        return self

    def where(self, **conditions: dict):
        if self.__tmp_query is None:
            raise InvalidQuery("Tmp query shold be not start from where")

        vars = [f"{key}={value}" for key, value in conditions.items()]
        sql_cond += " AND ".join(vars)

        self.__tmp_query += f" WHERE {sql_cond}"

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

    def join(self, other):
        pass
