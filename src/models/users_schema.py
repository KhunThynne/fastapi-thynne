import strawberry

from prisma.models import users

from .shared import StrawberryPydanticBase


@strawberry.experimental.pydantic.type(model=users, fields=["id", "username", "email"])
class UsersType(StrawberryPydanticBase):
    pass
