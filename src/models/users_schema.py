import strawberry

from prisma.models import users

from .shared import StrawberryPydanticBase


@strawberry.experimental.pydantic.type(model=users, all_fields=True)
class UsersType(StrawberryPydanticBase):
    pass
