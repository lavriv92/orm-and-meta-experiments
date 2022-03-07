from .lookup import is_lookup, lookup


def normalize_conditions(conditions: dict):
    normalized_conditions = []

    for field, value in conditions.items():
        if is_lookup(field):
            normalized_conditions.append(lookup(field, value))
        else:
            normalized_conditions.append(f"{field}={value}")

    return " AND ".join(normalized_conditions)
