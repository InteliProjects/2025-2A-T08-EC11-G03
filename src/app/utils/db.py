from typing import Optional
from prisma import Prisma

_prisma: Optional[Prisma] = None

def get_prisma() -> Prisma:
    global _prisma
    if _prisma is None:
        _prisma = Prisma()
    return _prisma

async def connect_prisma() -> None:
    prisma = get_prisma()
    if not prisma.is_connected():
        await prisma.connect()

async def disconnect_prisma() -> None:
    prisma = get_prisma()
    if prisma.is_connected():
        await prisma.disconnect()
