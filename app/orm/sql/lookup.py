from ..exceptions import UnsupportableLookup


def format_in_field(item):
    if isinstance(item, str):
        return f"{item!r}"

    return str(item)


def format_sequence(seq):
    return ", ".join(map(format_in_field, seq))


def lookup_in(field: str, value):
    return f"{field} IN ({format_sequence(value)}) "


def lookup_gt(field: str, value):
    return f"{field} > {value}"


def lookup_lt(field: str, value):
    return f"{field} < {value}"


def lookup_gte(field: str, value):
    return f"{field} >= {value}"


def lookup_lte(field: str, value):
    return f"{field} <= {value}"


def lookup_starts(field: str, value):
    return f"{field} LIKE '{value}%'"


def lookup_ends(field: str, value):
    return f"{field} LIKE '%{value}'"


def lookup_contains(field: str, value):
    return f"{field} LIKE '%{value}%'"


lookups = {
    "in": lookup_in,
    "gt": lookup_gt,
    "lt": lookup_lt,
    "lte": lookup_lte,
    "gte": lookup_gte,
    "starts": lookup_starts,
    "ends": lookup_ends,
    "contains": lookup_contains,
}


def is_lookup(field: str):
    index = field.find("__")

    return index > -1


def lookup(field: str, value):
    raw_field, prefix = field.split("__")
    lookup_func = lookups.get(prefix)

    if not lookup_func:
        raise UnsupportableLookup("lookup __{prefix} is unsupportable")

    return lookup_func(raw_field, value)
