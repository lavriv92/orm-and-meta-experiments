from ..exceptions import InvalidQuery
from ..utils import get_formatted_keys, get_keys, get_tablename
from .utils import normalize_conditions


class QueryBuilder:
    def __init__(self, model):
        self.__segments = []
        self.model = model

    @property
    def __table_name(self):
        return get_tablename(self.model)

    @property
    def __formatted_keys(self):
        return ", ".join(get_formatted_keys(self.model))

    def __format_values(self, instance):
        values = [f"{v!r}" for v in vars(instance).values()]

        return ", ".join(values)

    def create(self, instance):
        keys = ",".join(get_keys(instance.__class__))

        self.__segments.append(
            f"INSERT INTO {self.__table_name}({keys}) VALUES ({self.__format_values(instance)})"
        )
        return self

    def build(self):
        return " ".join(self.__segments)

    def select(self, fields):
        self.__segments.append(
            f"SELECT {self.__formatted_keys} FROM {self.__table_name}"
        )
        return self

    def where(self, **conditions: dict):
        if not self.__segments:
            raise InvalidQuery("Tmp query shold be not start from where")

        self.__segments.append(f"WHERE {normalize_conditions(conditions)}")

        return self

    def skip(self, number):
        if not self.__segments:
            raise InvalidQuery("Tmp query shold be not start from where")

        self.__segments.append(f"OFFSET {number}")

        return self

    def limit(self, limit):
        if not self.__segments:
            raise InvalidQuery("Tmp query is invalid")

        self.__segments.append(f"LIMIT {limit}")

        return self

    def join(self, other_model):
        pass
