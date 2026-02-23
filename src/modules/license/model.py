from typing import TYPE_CHECKING, Annotated

import strawberry

from prisma.models import license

from modules.base import StrawberryPydanticBase

if TYPE_CHECKING:
    from modules.product.model import ProductType
    from modules.user.model import UserType


@strawberry.experimental.pydantic.type(
    model=license,
    fields=["id", "key", "owner_id", "product_id", "activated_at", "expired_at"],
)
class LicenseType(StrawberryPydanticBase):
    users: list[Annotated["UserType", strawberry.lazy("modules.user.model")]] | None
    products: (
        list[Annotated["ProductType", strawberry.lazy("modules.product.model")]] | None
    )
