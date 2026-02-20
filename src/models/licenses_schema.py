import strawberry

from prisma.models import licenses

from .shared import StrawberryPydanticBase


@strawberry.experimental.pydantic.type(
    model=licenses,
    fields=["id", "key", "product_id", "owner_id", "activated_at", "expired_at"],
)
class LicensesType(StrawberryPydanticBase):
    pass
