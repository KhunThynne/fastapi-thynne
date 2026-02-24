import asyncio
import json

from collections.abc import AsyncGenerator

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

router = APIRouter()


async def log_generator() -> AsyncGenerator[str, None]:
    logs = [
        {"status": "starting", "progress": 10},
        {"status": "processing", "progress": 50},
        {"status": "completed", "progress": 100},
    ]
    for log in logs:
        # yield เป็น string ที่ลงท้ายด้วย \n เพื่อให้ Postman แยกบรรทัดได้
        yield json.dumps(log) + "\n"
        await asyncio.sleep(1)


@router.get("/logs")
async def stream_logs() -> StreamingResponse:
    return StreamingResponse(log_generator(), media_type="application/x-ndjson")
