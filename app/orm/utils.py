from cgitb import lookup
from typing import get_origin, get_args, Union


def is_optional(annotation):
    return get_origin(annotation) is Union and type(None) in get_args(annotation)


def get_origin_type(annotation):
    if is_optional(annotation):
        origin_type, _ = get_args(annotation)

        return origin_type

    origin_type = get_origin(annotation)

    if origin_type is None:
        return annotation

    return origin_type


def parse_connection_string(connection_string):
    protocol, database_url = connection_string.split("://")

    return {"engine": protocol, "url": database_url}


def get_tablename(model):
    if hasattr(model, "__tablename__"):
        return model.__tablename__

    return model.__name__


def get_keys(model):
    keys = vars(model).get("__annotations__", {}).keys()
    formatted_keys = [f"{key}" for key in keys]

    return formatted_keys


def get_selection_keys(model):
    return ["id"] + get_keys(model)
