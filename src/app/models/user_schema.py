from dataclasses import dataclass

import strawberry

from sqlmodel import Field, SQLModel


class UserBase:
    username: str
    email: str


class UserTable(UserBase, SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)


@strawberry.type
@dataclass
class UserType(UserBase):
    id: int
