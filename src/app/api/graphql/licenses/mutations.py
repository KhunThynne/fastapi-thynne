import uuid

from datetime import UTC, datetime
from uuid import UUID

import strawberry

from core.db import prisma
from modules.license.model import LicenseType
from utils.license import generate_product_key


@strawberry.type
class LicenseMutation:
    @strawberry.mutation
    async def create_license(
        self,
        product_id: UUID,
        key: str | None = None,
    ) -> LicenseType:
        final_key = key if key else generate_product_key()
        new_id = str(uuid.uuid4())

        new_license = await prisma.license.create(
            data={"id": new_id, "key": final_key, "product_id": str(product_id)}
        )
        return LicenseType.from_pydantic(new_license)

    @strawberry.mutation
    async def delete_license(self, id: UUID) -> bool:
        deleted = await prisma.license.delete_many(where={"id": str(id)})
        return deleted > 0

    @strawberry.mutation
    async def revoke_license(self, key: str) -> bool:
        updated = await prisma.license.update_many(
            where={"key": key}, data={"expired_at": datetime.now(UTC)}
        )
        return updated > 0
