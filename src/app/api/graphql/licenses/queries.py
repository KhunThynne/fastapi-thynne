from datetime import UTC, datetime
from typing import cast

import strawberry

from prisma.types import LicenseWhereInput

from core.db import prisma_client
from modules.license.model import LicenseKeyArg, LicenseType


@strawberry.input
class LicenseWhereInputType:
    id: str | None = None
    key: str | None = None
    user_id: str | None = None
    product_id: str | None = None
    pass


@strawberry.type
class LicenseQuery:
    @strawberry.field
    async def get_licenses(
        self,
        where: LicenseWhereInputType | None = None,
        take: int | None = 100,
        skip: int | None = 0,
    ) -> list[LicenseType]:
        where = cast(LicenseWhereInput, where)
        license = await prisma_client.license.find_many(
            where=where or {},
            take=take,
            skip=skip,
        )
        return [LicenseType.from_pydantic(li) for li in license]

    @strawberry.field
    async def validate_license(self, key: LicenseKeyArg) -> LicenseType:
        license_obj = await prisma_client.license.find_first(where={"key": key})
        if not license_obj:
            raise Exception("INVALID_LICENSE: The provided key does not exist.")
        if license_obj.expired_at and license_obj.expired_at < datetime.now(UTC):
            raise Exception("INVALID_LICENSE: The provided key is expired.")
        return LicenseType.from_pydantic(license_obj)
