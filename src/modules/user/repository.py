from modules.base import BaseRepository
from prisma.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__("user")

    pass
