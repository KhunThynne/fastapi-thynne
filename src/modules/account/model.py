from typing import TYPE_CHECKING, Annotated

import strawberry

from modules.base import StrawberryPydanticBase
from prisma.models import Account

if TYPE_CHECKING:
    from modules.user.model import UserType


@strawberry.experimental.pydantic.type(
    model=Account,
)
class AccountType(StrawberryPydanticBase):
    id: strawberry.auto
    userId: strawberry.auto
    type: strawberry.auto
    provider: strawberry.auto
    providerAccountId: strawberry.auto
    user: Annotated["UserType", strawberry.lazy("modules.user.model")] | None = None
