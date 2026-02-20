import strawberry

from prisma.enums import productstypeenum
from prisma.models import products

from .shared import StrawberryPydanticBase

ProductsTypeEnum = strawberry.enum(productstypeenum)


@strawberry.experimental.pydantic.type(model=products, all_fields=True)
class ProductsType(StrawberryPydanticBase):
    pass
