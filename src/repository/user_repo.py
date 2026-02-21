# src/repositories/user_repo.py
from prisma.models import User

from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__("user")

    async def get_user_with_accounts(self, user_id: str) -> User | None:
        return await self.model.find_unique(
            where={"id": user_id}, include={"accounts": True}
        )
