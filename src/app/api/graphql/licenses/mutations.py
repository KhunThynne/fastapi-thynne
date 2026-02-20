import uuid

from datetime import UTC, datetime
from uuid import UUID

import strawberry

from core.db import prisma
from models.gql_types import LicensesType
from utils.license import generate_product_key


@strawberry.type
class LicenseMutation:
    @strawberry.mutation
    async def create_license(
        self,
        product_id: UUID,
        key: str | None = None,
    ) -> LicensesType:
        final_key = key if key else generate_product_key()
        new_id = str(uuid.uuid4())

        new_license = await prisma.licenses.create(
            data={"id": new_id, "key": final_key, "product_id": str(product_id)}
        )
        return LicensesType.from_pydantic(new_license)

    @strawberry.mutation
    async def delete_license(self, id: UUID) -> bool:
        deleted = await prisma.licenses.delete_many(where={"id": str(id)})
        return deleted > 0

    @strawberry.mutation
    async def revoke_license(self, key: str) -> bool:
        updated = await prisma.licenses.update_many(
            where={"key": key}, data={"expired_at": datetime.now(UTC)}
        )
        return updated > 0
