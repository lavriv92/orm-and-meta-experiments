def validator(field_name):
    def wrapper(func):
        setattr(func, "__validated_field__", field_name)

        return func

    return wrapper
