import strawberry

from core.db import prisma
from models.products_schema import ProductsType


@strawberry.type
class ProductsQuery:
    @strawberry.field
    async def get_products(self) -> list[ProductsType]:
        products = await prisma.products.find_many()
        return [ProductsType.from_pydantic(p) for p in products]

    @strawberry.field
    async def get_product(self, id: str) -> ProductsType | None:
        product = await prisma.products.find_unique(where={"id": id})
        if product:
            return ProductsType.from_pydantic(product)
        return None
