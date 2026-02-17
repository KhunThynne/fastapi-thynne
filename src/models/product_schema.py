import enum
import uuid

from dataclasses import dataclass
from uuid import UUID

import strawberry

from sqlmodel import Field, SQLModel


class ProductTypeEnum(enum.StrEnum):
    PRO = "pro"
    LITE = "lite"
    FREE = "free"


@dataclass
class ProductBase:
    name: str
    type: ProductTypeEnum  # e.g., "Pro", "Lite"
    duration_days: int


class ProductTable(ProductBase, SQLModel, table=True):
    __tablename__ = "products"
    id: UUID = Field(
        default_factory=uuid.uuid4, primary_key=True, index=True, nullable=False
    )
    name: str = Field(index=True)


@strawberry.type
@dataclass
class ProductType(ProductBase):
    id: UUID
