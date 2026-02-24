from prisma import Prisma

prisma_client = Prisma(auto_register=True)


async def init_db() -> None:
    """Initialize database connection"""
    if not prisma_client.is_connected():
        await prisma_client.connect()


async def close_db() -> None:
    """Close database connection"""
    if prisma_client.is_connected():
        await prisma_client.disconnect()
