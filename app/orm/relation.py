from enum import Enum

from typing import Optional
from .exceptions import ModelIsNotExists, IsNotModel
from .model import Model

from .fields import RelationField


class RelationTypes(Enum):
    ONE_TO_ONE = 0
    ONE_TO_MANY = 0


def get_model_name(model):
    if isinstance(model, str):
        return model

    if issubclass(model, Model):
        return model.__name__

    raise IsNotModel("Decorated class is not a model")


def generate_relation_field_name(model_name, relation_field=None):
    if relation_field:
        return relation_field

    return f"{model_name.lower()}_id"


def relation(
    model,
    relation_type=RelationTypes.ONE_TO_MANY,
    relation_field=None,
    lookup_field=None,
):
    def decorator(cls):
        model_name = get_model_name(model)
        model_exists = any([model_name == m.__name__ for m in Model.__subclasses__()])

        if not model_exists:
            raise ModelIsNotExists(f"{model_name} is not registered")

        annotations = vars(cls).get("__annotations__", {})
        field_name = generate_relation_field_name(model_name, relation_field)

        annotations[field_name] = Optional[int]

        setattr(cls, model_name.lower(), RelationField())

        return cls

    return decorator
