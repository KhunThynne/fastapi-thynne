from generated.prisma.models import user
from modules.base import BaseRepository


class UserRepository(BaseRepository[user]):
    def __init__(self) -> None:
        super().__init__("user")

    pass
