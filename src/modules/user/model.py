from typing import TYPE_CHECKING, Annotated

import strawberry

from modules.base import StrawberryPydanticBase
from prisma.models import User

if TYPE_CHECKING:
    from modules.account.model import AccountType


@strawberry.experimental.pydantic.input(model=User)
class UserCreateInput(StrawberryPydanticBase):
    username: strawberry.auto
    email: strawberry.auto
    role: strawberry.auto


@strawberry.experimental.pydantic.type(model=User)
class UserType(StrawberryPydanticBase):
    id: strawberry.auto
    username: strawberry.auto
    email: strawberry.auto
    role: strawberry.auto
    accounts: (
        list[Annotated["AccountType", strawberry.lazy("modules.account.model")]] | None
    ) = None
