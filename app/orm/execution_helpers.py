from .sql.query_builder import QueryBuilder


def select(model):
    QueryBuilder(model).select()
