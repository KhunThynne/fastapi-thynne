from typing import TYPE_CHECKING, Annotated

import strawberry

from modules.base import StrawberryPydanticBase
from prisma.models import Account

if TYPE_CHECKING:
    from modules.user.model import UserType


@strawberry.experimental.pydantic.type(
    model=Account,
    fields=["id", "userId", "type", "provider", "providerAccountId"],
)
class AccountType(StrawberryPydanticBase):
    user: list[Annotated["UserType", strawberry.lazy("modules.user.model")]] | None = (
        None
    )
