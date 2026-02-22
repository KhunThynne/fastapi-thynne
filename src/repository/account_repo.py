from uuid import UUID

from prisma.models import Account

from .shared import BaseRepository


class AccountRepository(BaseRepository[Account]):
    def __init__(self) -> None:
        super().__init__("account")

    async def get_accounts(self) -> list[Account]:
        return await self.model.find_many(take=100)

    async def get_account(
        self, id: UUID | None = None, provider_account_id: str | None = None
    ) -> Account | None:
        if id is not None:
            return await self.model.find_unique(where={"id": str(id)})
        elif provider_account_id is not None:
            return await self.model.find_first(
                where={"providerAccountId": provider_account_id}
            )
        return None
