import json
from collections import defaultdict

from .utils import is_optional, get_origin_type
from .exceptions import ValidationError


class ModelMeta(type):
    @property
    def __class_variables(self):
        return vars(self)

    @property
    def __field_annotations(self):
        return self.__class_variables.get("__annotations__", {})

    def __get_validators(self, field_name):
        return (
            validator
            for validator in self.__class_variables.values()
            if getattr(validator, "__validated_field__", None) == field_name
        )

    def __call__(self, *args, **kwargs):
        for field_name, annotation in self.__field_annotations.items():
            value = kwargs.get(field_name)

            try:
                if not is_optional(annotation) and value is None:
                    raise ValueError(f"Field {field_name!r} is required")

                if value is None:
                    continue

                origin_type = get_origin_type(annotation)

                if type(value) is not origin_type:
                    raise TypeError(
                        f"Expected value should be {origin_type.__name__!r} but get {type(value).__name__!r}"
                    )

            except (TypeError, ValueError) as e:
                self._errors[field_name].append(e)
                continue

            for validator in self.__get_validators(field_name):
                try:
                    validator(self, value, *args, **kwargs)
                except ValueError as e:
                    self._errors[field_name].append(e)
                    continue

        if self._errors:
            raise ValidationError("Validation message", error_messages=self._errors)

        return super().__call__(*args, **kwargs)


class Model(metaclass=ModelMeta):
    _errors = defaultdict(list)

    def __init__(self, *args, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    @property
    def dict(self):
        return vars(self)

    @property
    def json(self):
        return json.dumps(self.dict)
