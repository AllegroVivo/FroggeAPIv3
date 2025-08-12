from __future__ import annotations

from sqlalchemy import Column, BigInteger, TIMESTAMP, func, Integer, Boolean
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from sqlalchemy.orm import declarative_base
import json
from sqlalchemy.types import TypeDecorator, TEXT
################################################################################

__all__ = (
    "BaseModel",
    "ArrayOrJSON",
    "NormalizedBoolean"
)

################################################################################

BaseModel = declarative_base()

################################################################################
class ArrayOrJSON(TypeDecorator):
    """Uses Postgres ARRAY for native arrays, JSON (or TEXT) fallback elsewhere."""
    impl = TEXT
    cache_ok = True

    def __init__(self, inner_type=Integer, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inner_type = inner_type  # E.g., Integer or String

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(PG_ARRAY(self.inner_type))
        else:
            return dialect.type_descriptor(TEXT())  # Stored as JSON string in SQLite

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if dialect.name == "postgresql":
            return value  # Pass native list directly to Postgres
        return json.dumps(value)  # Store as JSON text elsewhere

    def process_result_value(self, value, dialect):
        if value is None:
            return []
        if dialect.name == "postgresql":
            return value  # Already a native Python list
        return json.loads(value)  # Convert JSON string back to list

################################################################################
class NormalizedBoolean(TypeDecorator):
    """
    A cross-dialect BOOLEAN type.
    - Stores as INTEGER(0/1) in SQLite.
    - Uses native BOOLEAN in Postgres (or other dialects).
    """
    impl = Boolean
    cache_ok = True

    def load_dialect_impl(self, dialect):
        # SQLite has no BOOLEAN → fallback to Integer
        if dialect.name == "sqlite":
            return dialect.type_descriptor(Integer())
        return dialect.type_descriptor(Boolean())

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        return 1 if bool(value) else 0 if dialect.name == "sqlite" else bool(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return bool(value)

################################################################################
