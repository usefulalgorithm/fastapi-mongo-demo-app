from beanie import Document
from pydantic import Field

from test_mongo_project.web.api.user.schema import UserBase


class UserModel(Document, UserBase):
    hashed_password: str = Field(exclude=True)
