from typing import TYPE_CHECKING, Annotated

import strawberry

from prisma.models import product

from modules.base import StrawberryPydanticBase

if TYPE_CHECKING:
    from modules.license.model import LicenseType


@strawberry.experimental.pydantic.type(
    model=product,
    fields=["id", "type", "name", "duration_days"],
)
class ProductType(StrawberryPydanticBase):
    licenses: (
        list[Annotated["LicenseType", strawberry.lazy("modules.license.model")]] | None
    )
