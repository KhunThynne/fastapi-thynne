import strawberry

from app.core.db import async_session_maker
from app.models.user_schema import UserTable, UserType


@strawberry.type
class UserMutation:
    @strawberry.mutation
    async def create_user(self, username: str, email: str) -> UserType:
        # 1. เปิด Session เพื่อคุยกับ Database
        async with async_session_maker() as session:
            # 2. สร้าง Instance ของ UserTable (SQLModel) เพื่อเตรียมบันทึก
            new_user = UserTable(username=username, email=email)

            # 3. สั่งบันทึกลง DB
            session.add(new_user)
            await session.commit()

            # 4. Refresh เพื่อเอาข้อมูลที่ DB สร้างให้ (เช่น id) กลับมา
            await session.refresh(new_user)

            # 5. ส่งคืนข้อมูลในรูปแบบ UserType (GraphQL)
            return UserType(
                id=new_user.id,  # type: ignore (เพราะเรารู้ว่า id ถูกสร้างแล้ว)
                username=new_user.username,
                email=new_user.email,
            )
