import uuid

import strawberry

from core.db import prisma
from models.products_schema import ProductsType, ProductsTypeEnum


@strawberry.type
class ProductsMutation:
    @strawberry.mutation
    async def create_product(
        self, name: str, type: ProductsTypeEnum, duration_days: int | None = 0
    ) -> ProductsType:
        try:
            new_id = str(uuid.uuid4())
            new_product = await prisma.products.create(
                data={
                    "id": new_id,
                    "name": name,
                    "type": type,
                    "duration_days": duration_days or 0,
                }
            )
            return ProductsType.from_pydantic(new_product)
        except Exception as e:
            import traceback

            with open("graphql_error.txt", "w") as f:
                traceback.print_exc(file=f)
            raise e

    @strawberry.mutation
    async def delete_product(self, id: str) -> bool:
        product = await prisma.products.delete(where={"id": id})
        return product is not None
