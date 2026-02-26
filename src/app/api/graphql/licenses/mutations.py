from datetime import UTC, datetime
from uuid import UUID

import strawberry

from core.db import prisma_client
from modules.license.model import LicenseCreateInputType, LicenseType
from utils.license import generate_product_key


@strawberry.type
class LicenseMutation:
    @strawberry.mutation
    async def create_license(
        self,
        data: LicenseCreateInputType,
    ) -> LicenseType:
        final_key = data.key or generate_product_key()
        if len(final_key) != 36:
            raise Exception(
                f"License key must be exactly 36 characters form {len(final_key)}"
            )
        new_license = await prisma_client.license.create(
            data={
                "key": final_key,
                "product_id": str(data.product_id),
                "activated_at": datetime.now(UTC),
            }
        )
        return LicenseType.from_pydantic(new_license)

    @strawberry.mutation
    async def delete_license(self, id: UUID) -> bool:
        deleted = await prisma_client.license.delete_many(where={"id": str(id)})
        return deleted > 0

    @strawberry.mutation
    async def revoke_license(self, key: str) -> bool:
        updated = await prisma_client.license.update_many(
            where={"key": key}, data={"expired_at": datetime.now(UTC)}
        )
        return updated > 0

    @strawberry.mutation
    async def update_license(
        self, id: UUID, data: strawberry.scalars.JSON
    ) -> LicenseType:

        update_data = {
            k: v for k, v in strawberry.asdict(data).items() if v is not None
        }

        if "product_id" in update_data:
            update_data["product_id"] = str(update_data["product_id"])
        if "user_id" in update_data:
            update_data["user_id"] = str(update_data["user_id"])

        updated = await prisma_client.license.update(
            where={"id": str(id)},
            data=update_data,  # type: ignore
        )

        return LicenseType.from_pydantic(updated)
