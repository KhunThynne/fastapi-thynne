from modules.base import BaseRepository
from prisma.models import Account


class AccountRepository(BaseRepository[Account]):
    def __init__(self) -> None:
        super().__init__("account")

    pass
