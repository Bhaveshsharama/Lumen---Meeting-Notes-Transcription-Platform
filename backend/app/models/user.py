"""
models/user.py — User ORM model.

SRP: This model maps exclusively to the `users` table. The logged-in owner
of meetings. Currently a single seeded user, but modeled as a real table
so swapping in authentication later doesn't require a schema migration.

Relationship: User.meetings → list of Meeting objects (one-to-many).
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # One user owns many meetings (relationship, not a column)
    meetings = relationship("Meeting", back_populates="owner", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User id={self.id} name={self.name!r}>"
