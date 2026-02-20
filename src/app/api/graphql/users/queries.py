from uuid import UUID

import strawberry

from core.db import prisma
from models.gql_types import UsersType


@strawberry.type
class UsersQuery:
    @strawberry.field
    async def get_users(self, info: strawberry.Info) -> list[UsersType]:
        users_db = await prisma.users.find_many(take=100)
        return [UsersType.from_pydantic(u) for u in users_db]

    @strawberry.field
    async def get_user(
        self, info: strawberry.Info, id: UUID | None = None, username: str | None = None
    ) -> UsersType | None:
        user = None
        if id is not None:
            user = await prisma.users.find_unique(where={"id": str(id)})
        elif username is not None:
            user = await prisma.users.find_unique(where={"username": username})

        if user:
            return UsersType.from_pydantic(user)
        return None
