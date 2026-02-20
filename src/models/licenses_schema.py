import strawberry

from prisma.models import licenses

from .shared import StrawberryPydanticBase


@strawberry.experimental.pydantic.type(model=licenses, all_fields=True)
class LicensesType(StrawberryPydanticBase):
    pass
