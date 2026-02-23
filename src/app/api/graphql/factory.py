from typing import Any, Self, Literal  # noqa: I001, UP035
from uuid import UUID
from enum import Enum
import strawberry
import sys


class GqlMode(Enum):
    QUERY = "query"
    MUTATION = "mutation"


CRUDMode = Literal["query", "mutation"]


def strawberry_crud(  # noqa: ANN201
    mode: CRUDMode,
    gql_type: type[Any],
    repo: Any,  # noqa: ANN401
    input_fields: type[Any] | None = None,
    prefix: str = "",
):  # noqa: ANN201, ANN401
    def wrapper(cls):  # noqa: ANN001, ANN202
        name = prefix if prefix else gql_type.__name__.replace("Type", "").lower()
        # auto_input_type = None
        # if input_fields and mode == "mutation":
        #     auto_input_type = create_dynamic_input(name, input_fields)
        current_module = sys.modules[cls.__module__]

        async def get_all(self: Self, info: strawberry.Info) -> list[gql_type]:
            items = await repo.get_all()
            print(items)
            return [gql_type.from_pydantic(i) for i in items]

        async def get_one(
            self: Self,
            info: strawberry.Info,
            id: UUID | None = None,
            **kwargs: None,
        ) -> gql_type | None:
            search_params = {"id": str(id)} if id else kwargs
            item = await repo.find_unique_or_any(**search_params)
            return gql_type.from_pydantic(item) if item else None

        async def create_item(
            self: Self,
            info: strawberry.Info,
            data: input_fields if input_fields else strawberry.scalars.JSON,
        ) -> gql_type:  # noqa: E501
            # 1. เช็คว่ามี data ส่งมาจริงไหม
            if data is None:
                raise Exception("Input data is missing in Variables")
            # 2. สั่งสร้างข้อมูล (ตรวจสอบว่า repo คือ prisma.user หรือไม่)
            item = await repo.create(data=data)

            # 3. เช็คว่าสร้างสำเร็จไหม ก่อนจะไป .from_pydantic
            if item is None:
                raise Exception("Failed to create item in database")

            return gql_type.from_pydantic(item)

        async def update_item(
            self: Self,
            info: strawberry.Info,
            id: UUID,
            data: strawberry.scalars.JSON,
        ) -> gql_type:
            item = await repo.update(str(id), data)
            return gql_type.from_pydantic(item)

        async def delete_item(self: Self, info: strawberry.Info, id: UUID) -> bool:
            return await repo.delete(str(id))

        async def create_many(
            self: Self, info: strawberry.Info, data: list[strawberry.scalars.JSON]
        ) -> list[gql_type]:

            items = await repo.create_many(data)
            return [gql_type.from_pydantic(i) for i in items]

        async def update_many(
            self: Self, info: strawberry.Info, data: list[strawberry.scalars.JSON]
        ) -> list[gql_type]:

            items = await repo.update_many(data)
            return [gql_type.from_pydantic(i) for i in items]

        async def delete_many(
            self: Self, info: strawberry.Info, ids: list[UUID]
        ) -> int:

            str_ids = [str(id) for id in ids]
            count = await repo.delete_many(str_ids)
            return count

        func_name = f"create_{name}_func"
        setattr(current_module, func_name, create_item)
        if mode == "query":
            setattr(cls, f"get_{name}s", strawberry.field(get_all))
            setattr(cls, f"get_{name}", strawberry.field(get_one))

        elif mode == "mutation":
            setattr(cls, f"create_{name}", strawberry.mutation(create_item))
            setattr(cls, f"update_{name}", strawberry.mutation(update_item))
            setattr(cls, f"delete_{name}", strawberry.mutation(delete_item))
            setattr(cls, f"create_{name}s", strawberry.mutation(create_many))
            setattr(cls, f"update_{name}s", strawberry.mutation(update_many))
            setattr(cls, f"delete_{name}s", strawberry.mutation(delete_many))
        return strawberry.type(cls)

    return wrapper
