from generated.prisma.models import License
from modules.base import BaseRepository


class LicenseRepository(BaseRepository[License]):
    def __init__(self) -> None:
        super().__init__("license")

    pass
