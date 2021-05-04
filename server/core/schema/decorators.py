from functools import wraps

from graphql_relay import from_global_id


def decode_id(*id_fields_names):
    """Convert provided input names from global ID to regular (django) ID"""

    def outer(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            for field_name in id_fields_names:
                value = kwargs.get(field_name)

                if not value:
                    continue

                if isinstance(value, list):
                    kwargs[field_name] = [from_global_id(v)[1] for v in value]
                else:
                    kwargs[field_name] = from_global_id(value)[1]

            return fn(*args, **kwargs)

        return inner

    return outer
