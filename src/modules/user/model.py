from typing import TYPE_CHECKING, Annotated

import strawberry

from prisma.models import User

from modules.base import StrawberryPydanticBase

if TYPE_CHECKING:
    from modules.license.model import LicenseType


@strawberry.experimental.pydantic.type(
    model=User,
)
class UserType(StrawberryPydanticBase):
    id: strawberry.auto
    username: strawberry.auto
    email: strawberry.auto
    licenses: Annotated["LicenseType", strawberry.lazy("modules.license.model")] | None
