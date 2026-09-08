"""
models/base.py — Declarative base for all SQLAlchemy models.

Single Responsibility: this module's only job is to provide the shared Base
class that every model inherits from. No table definitions live here.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all ORM models. All models inherit from this."""
    pass
