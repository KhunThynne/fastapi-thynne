from uuid import UUID

import strawberry

from core.db import prisma
from modules.license.model import LicenseType


@strawberry.type
class LicensesQuery:
    @strawberry.field
    async def get_licenses(self) -> list[LicenseType]:
        license = await prisma.license.find_many(take=100)
        return [LicenseType.from_pydantic(li) for li in license]

    @strawberry.field
    async def get_license_by_product_id(self, product_id: UUID) -> LicenseType | None:
        license_obj = await prisma.license.find_first(
            where={"product_id": str(product_id)}
        )
        if license_obj:
            return LicenseType.from_pydantic(license_obj)
        return None

    @strawberry.field
    async def get_license(self, key: str) -> LicenseType | None:
        license_obj = await prisma.license.find_first(where={"key": key})
        if license_obj:
            return LicenseType.from_pydantic(license_obj)
        return None
