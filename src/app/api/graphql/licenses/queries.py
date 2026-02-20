from uuid import UUID

import strawberry

from core.db import prisma
from models.licenses_schema import LicensesType


@strawberry.type
class LicensesQuery:
    @strawberry.field
    async def get_licenses(self) -> list[LicensesType]:
        licenses = await prisma.licenses.find_many(take=100)
        return [LicensesType.from_pydantic(li) for li in licenses]

    @strawberry.field
    async def get_license_by_product_id(self, product_id: UUID) -> LicensesType | None:
        license_obj = await prisma.licenses.find_first(
            where={"product_id": str(product_id)}
        )
        if license_obj:
            return LicensesType.from_pydantic(license_obj)
        return None

    @strawberry.field
    async def get_license(self, key: str) -> LicensesType | None:
        license_obj = await prisma.licenses.find_first(where={"key": key})
        if license_obj:
            return LicensesType.from_pydantic(license_obj)
        return None
