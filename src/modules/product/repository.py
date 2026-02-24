from prisma.models import Product

from modules.base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self) -> None:
        super().__init__("product")

    pass
