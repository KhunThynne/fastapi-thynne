from typing import Any  # noqa: UP035
from uuid import UUID

import strawberry


def strawberry_crud(gql_type: type[Any], repo: Any, prefix: str = ""):  # noqa: ANN201, ANN401
    """
    Decorator สำหรับฉีด CRUD methods เข้าไปใน class อัตโนมัติ
    prefix: ใช้สำหรับกรณีอยากได้ชื่อฟังก์ชันแบบ get_admin_users (ถ้าต้องการ)
    """

    def wrapper(cls):  # noqa: ANN001, ANN202
        model_name = gql_type.__name__.replace("Type", "").lower()

        # 1. Dynamic Method: Get All
        async def get_all(self, info: strawberry.Info) -> list[gql_type]:  # noqa: ANN001
            items = await repo.get_all()
            return [gql_type.from_pydantic(i) for i in items]

        # 2. Dynamic Method: Get Single (By ID or Unique Key)
        async def get_one(
            self,  # noqa: ANN001
            info: strawberry.Info,  # noqa: ANN001
            id: UUID | None = None,  # noqa: ANN001, ANN003
            **kwargs,  # noqa: ANN001, ANN003
        ) -> gql_type | None:
            search_params = {"id": str(id)} if id else kwargs
            item = await repo.find_unique_or_any(**search_params)
            return gql_type.from_pydantic(item) if item else None

        # ฉีด method เข้าไปใน class พร้อมกำหนดชื่อแบบ dynamic
        setattr(cls, f"get_{model_name}s", strawberry.field(get_all))
        setattr(cls, f"get_{model_name}", strawberry.field(get_one))

        # คืนค่า class ที่ถูกฉีด field แล้วและหุ้มด้วย @strawberry.type
        return strawberry.type(cls)

    return wrapper
