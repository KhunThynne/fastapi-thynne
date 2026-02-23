from typing import TYPE_CHECKING, Annotated

import strawberry

from modules.base import StrawberryPydanticBase
from prisma.models import User

if TYPE_CHECKING:
    from modules.account.model import AccountType


@strawberry.experimental.pydantic.input(
    model=User, fields=["username", "email", "role"]
)
class UserCreateInput(StrawberryPydanticBase):
    pass


@strawberry.experimental.pydantic.type(
    model=User, fields=["id", "username", "email", "role"]
)
class UserType(StrawberryPydanticBase):
    accounts: (
        list[Annotated["AccountType", strawberry.lazy("modules.account.model")]] | None
    ) = None
