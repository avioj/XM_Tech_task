from sqlalchemy import inspect
from enum import Enum


def object_as_dict(obj):
    result = {c.key: getattr(obj, c.key)
              for c in inspect(obj).mapper.column_attrs}
    return {k: v if not isinstance(v, Enum) else str(v) for k, v in result.items()}
