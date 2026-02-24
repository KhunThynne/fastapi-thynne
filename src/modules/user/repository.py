from generated.prisma.models import User

from modules.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self) -> None:
        super().__init__("user")

    pass
