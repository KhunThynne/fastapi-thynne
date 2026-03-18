from typing import TYPE_CHECKING, Annotated

import strawberry

from prisma.models import Product

from modules.base import StrawberryPydanticBase

if TYPE_CHECKING:
    from modules.license.model import LicenseType


@strawberry.experimental.pydantic.type(model=Product)
class ProductType(StrawberryPydanticBase):
    id: strawberry.auto
    type: strawberry.auto
    name: strawberry.auto
    licenses: Annotated["LicenseType", strawberry.lazy("modules.license.model")] | None
