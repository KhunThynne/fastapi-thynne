from typing import TYPE_CHECKING, Annotated

import strawberry

from prisma.models import User

from .shared import StrawberryPydanticBase

if TYPE_CHECKING:
    from .account import AccountType


@strawberry.experimental.pydantic.type(
    model=User, fields=["id", "username", "email", "role"]
)
class UsersType(StrawberryPydanticBase):
    accounts: list[Annotated["AccountType", strawberry.lazy(".account")]]
