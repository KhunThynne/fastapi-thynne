from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")

# 2. สร้างตัวแปรสำหรับจำ Type ของ Return Value
R = TypeVar("R")


# 3. ระบุว่ารับฟังก์ชันที่ใช้ P และคืนค่า R -> แล้วส่งกลับฟังก์ชันหน้าตาแบบเดิม
def test(role: str) -> Callable[[Callable[P, R]], Callable[P, R]]:

    # ชั้นที่ 2: Decorator ตัวจริง -> รับฟังก์ชันเป้าหมาย (func)
    def decorator(func: Callable[P, R]) -> Callable[P, R]:

        # ชั้นที่ 3: Wrapper -> รับ Argument ของฟังก์ชันเป้าหมาย (*args, **kwargs)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            print(f"--- ก่อนทำงาน (ตั้งค่า Role เป็น: {role}) ---")

            # ยัด Role ที่ได้จากชั้นที่ 1 ส่งต่อให้ฟังก์ชันเป้าหมาย (ชั้นที่ 3)
            kwargs["role"] = role

            # สั่งให้ฟังก์ชันเป้าหมายทำงาน
            result = func(*args, **kwargs)

            print("--- หลังทำงานเสร็จ ---")
            return result

        return wrapper  # คืนค่าชั้นที่ 3 ออกไปให้ชั้นที่ 2

    return decorator  # คืนค่าชั้นที่ 2 ออกไปให้ชั้นที่ 1


class Test:
    def __init__(self, func: Callable[P, R]) -> None:
        self.count = 0
        self.func = func

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        self.count += 1
        result = self.func(*args, **kwargs)
        return result.upper()


@Test
class hello:
    def __init__(self, func: Callable[P, R]) -> None:
        super().__init__()
        self.count = 0
        self.func = func

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        self.count += 1
        result = self.func(*args, **kwargs)
        return result.upper()
