# from typing import TYPE_CHECKING, Annotated

import strawberry

from generated.prisma.models import License
from modules.base import StrawberryPydanticBase

# if TYPE_CHECKING:
#     from modules.user.model import UserType


@strawberry.experimental.pydantic.type(
    model=License,
    fields=["id"],
)
class LicenseType(StrawberryPydanticBase):
    pass
    # user: list[Annotated["UserType",
    # strawberry.lazy("modules.user.model")]] |
    #  None = (
    #     None
    # )
