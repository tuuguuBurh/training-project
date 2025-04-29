import uuid

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import validates

from app.db.base_class import Base
from app.models.default import Default


class User(Base, Default):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, index=True, nullable=False, key="email", unique=True)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="True")

    @validates("email")
    def convert_lower(self, key, value):
        return value.strip().lower()
