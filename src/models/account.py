from typing import TYPE_CHECKING, Annotated

import strawberry

from prisma.models import Account

from .shared import StrawberryPydanticBase

if TYPE_CHECKING:
    from .user import UsersType


@strawberry.experimental.pydantic.type(
    model=Account,
    fields=["id", "userId", "type", "provider", "providerAccountId"],
)
class AccountType(StrawberryPydanticBase):
    user: list[Annotated["UsersType", strawberry.lazy("models.user")]]
