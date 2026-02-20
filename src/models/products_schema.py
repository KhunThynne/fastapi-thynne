import strawberry

from prisma.enums import productstypeenum
from prisma.models import products

from .shared import StrawberryPydanticBase

ProductsTypeEnum = strawberry.enum(productstypeenum)


@strawberry.experimental.pydantic.type(
    model=products, fields=["id", "name", "type", "duration_days"]
)
class ProductsType(StrawberryPydanticBase):
    pass
