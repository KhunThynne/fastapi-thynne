from prisma.models import product

from modules.base import BaseRepository


class ProductRepository(BaseRepository[product]):
    def __init__(self) -> None:
        super().__init__("license")

    pass
