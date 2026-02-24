from typing import TYPE_CHECKING, Annotated

import strawberry

from prisma.models import User

from modules.base import StrawberryPydanticBase

if TYPE_CHECKING:
    from modules.license.model import LicenseType


@strawberry.experimental.pydantic.type(
    model=User,
    fields=["id", "username", "email"],
)
class UserType(StrawberryPydanticBase):
    licenses: (
        list[Annotated["LicenseType", strawberry.lazy("modules.license.model")]] | None
    )
