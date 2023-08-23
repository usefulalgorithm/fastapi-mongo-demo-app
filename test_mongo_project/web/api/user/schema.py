from typing import Optional

from bson import ObjectId
from pydantic import (
    BaseModel,
    Field,
    FieldSerializationInfo,
    field_serializer,
    field_validator,
)


class UserBase(BaseModel):
    name: str
    email: Optional[str] = None
    is_active: bool = True


class UpdatePassword(BaseModel):
    password: str = Field(serialization_alias="hashed_password")

    @field_serializer("password")
    def hash_password(self, password: str, _info: FieldSerializationInfo) -> str:
        return f"this is so hashed!!!!{password}"


class UserCreate(UserBase, UpdatePassword):
    pass


class UserView(UserBase):
    id: str

    @field_validator("id", mode="before")
    @classmethod
    def parse_object_id(cls, v: ObjectId) -> str:
        return str(v)
