import uuid

from uuid import UUID

import strawberry

from core.db import prisma
from models.gql_types import UsersType


@strawberry.type
class UsersMutation:
    @strawberry.mutation
    async def create_user(self, username: str, email: str) -> UsersType:
        new_id = str(uuid.uuid4())
        new_user = await prisma.users.create(
            data={"id": new_id, "username": username, "email": email}
        )
        return UsersType.from_pydantic(new_user)

    @strawberry.mutation
    async def delete_user(self, id: UUID) -> UUID:
        user = await prisma.users.delete(where={"id": str(id)})
        if user:
            return id
        raise Exception(f"User with id {id} not found")
