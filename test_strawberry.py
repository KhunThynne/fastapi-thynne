import strawberry
from prisma.models import users

@strawberry.experimental.pydantic.type(model=users, fields=['id', 'username', 'email'])
class UsersType:
    pass

print(UsersType)
