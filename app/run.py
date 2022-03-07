from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class OneOf(Validator):
    def __init__(self, *options) -> None:
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f"Expected {value!r} to be one of {self.options!r}")


class Number(Validator):
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError(f"Expected {value!r} to be int or float")

        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Expected {value!r} to be at least {self.min_value!r}")

        if self.max_value is not None and value < self.max_value:
            raise ValueError(f"Expected {value!r} to be more than {self.max_value!r}")


class String(Validator):
    def __init__(self, min_size=None, max_size=None, predicate=None):
        self.min_size = min_size
        self.max_size = max_size
        self.predicate = predicate

    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Expected {value!r} to be an str")

        if self.min_size is not None and len(value) < self.min_size:
            raise ValueError(
                f"Expected {value!r} to be no smaller then {self.min_size!r}"
            )

        if self.max_size is not None and len(value) > self.max_size:
            raise ValueError(f"Expected {value!r} to be bigger then {self.max_size!r}")

        if self.predicate is not None and not self.predicate(value):
            raise ValueError(f"Expected {value!r} to be true for {self.predicate!r}")


class Component:
    name = String(min_size=3, max_size=12, predicate=str.isupper)
    kind = OneOf("wood", "metal", "plastic")
    quantity = Number(min_value=0)

    def __init__(self, name, kind, quantity) -> None:
        self.name = name
        self.kind = kind
        self.quantity = quantity
