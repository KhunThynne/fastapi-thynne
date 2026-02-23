from typing import TYPE_CHECKING, Any, Generic, Self, TypeVar

from core.db import prisma

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model_name: str) -> None:
        self.model = getattr(prisma, model_name)

    async def get_all(self) -> list[T]:
        return await self.model.find_many()

    async def get_by_id(self, id: str) -> T | None:
        return await self.model.find_unique(where={"id": id})

    async def create(self, data: Any) -> T:  # noqa: ANN401
        return await self.model.create(data=data)

    async def update(self, id: str, data: Any) -> T | None:  # noqa: ANN401
        return await self.model.update(where={"id": id}, data=data)

    async def delete(self, id: str) -> T | None:
        return await self.model.delete(where={"id": id})


class StrawberryPydanticBase:
    if TYPE_CHECKING:

        @classmethod
        def from_pydantic(cls, model_instance: Any) -> Self: ...  # noqa: ANN401
