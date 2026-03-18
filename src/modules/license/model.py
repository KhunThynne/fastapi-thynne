from typing import TYPE_CHECKING, Annotated, cast

import strawberry

from prisma.models import License
from prisma.types import LicenseCreateInput

from modules.base import StrawberryPydanticBase

if TYPE_CHECKING:
    from modules.product.model import ProductType
    from modules.user.model import UserType


LicenseKeyArg = Annotated[
    str, strawberry.argument(description="The 36-character license key")
]


@strawberry.experimental.pydantic.type(model=License)
class LicenseType(StrawberryPydanticBase):
    id: strawberry.auto
    key: strawberry.auto
    user_id: strawberry.auto
    product_id: strawberry.auto
    activated_at: strawberry.auto
    expired_at: strawberry.auto
    user: Annotated["UserType", strawberry.lazy("modules.user.model")] | None
    product: Annotated["ProductType", strawberry.lazy("modules.product.model")] | None


@strawberry.input
class LicenseCreateInputType:
    product_id: str
    key: str | None = None

    def __init__(self, product_id: str, key: str | None = None) -> None:
        self.product_id = product_id
        self.key = key

    def to_prisma(self) -> LicenseCreateInput:
        return cast(LicenseCreateInput, self.__dict__)
