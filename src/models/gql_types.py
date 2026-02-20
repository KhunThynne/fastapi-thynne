import strawberry

from prisma.enums import productstypeenum
from prisma.models import licenses, products, users

from .shared import StrawberryPydanticBase

ProductsTypeEnum = strawberry.enum(productstypeenum)


@strawberry.experimental.pydantic.type(model=users, all_fields=True)
class UsersType(StrawberryPydanticBase):
    pass


@strawberry.experimental.pydantic.type(model=products, all_fields=True)
class ProductsType(StrawberryPydanticBase):
    # ถ้าใน products มี relation ไปหา licenses ให้ระบุแบบนี้เพื่อกัน Error
    licenses: list["LicensesType"] | None = None
    pass


@strawberry.experimental.pydantic.type(model=licenses, all_fields=True)
class LicensesType(StrawberryPydanticBase):
    # ระบุความสัมพันธ์กลับไปหาตัวข้างบน
    products: ProductsType | None = None
    users: UsersType | None = None
