from fastapi import FastAPI
import uvicorn
import sys
from pathlib import Path
from contextlib import asynccontextmanager
import os

# Ensure .env is loaded before anything else
def _load_dotenv_from_root():
    candidates = [
        Path(__file__).resolve().parents[2] / ".env",  # repo root
        Path(__file__).resolve().parents[1] / ".env",  # src root
        Path(__file__).resolve().parent / ".env",      # app dir
    ]
    for p in candidates:
        if p.exists():
            with p.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" in line:
                        k, v = line.split("=", 1)
                        v = v.strip().strip('"').strip("'")
                        os.environ.setdefault(k.strip(), v)
            break

try:
    _load_dotenv_from_root()
except Exception:
    pass

# Optional: make sure `src` is importable if running as a script
if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.utils.db import get_prisma, connect_prisma, disconnect_prisma
from app.controllers.animalsController import router as animals_router
from app.controllers.colarController import router as collar_router  # note: file named colarController

@asynccontextmanager
async def lifespan(app: FastAPI):
    prisma = get_prisma()
    await prisma.connect()
    app.state.prisma = prisma
    try:
        yield
    finally:
        await prisma.disconnect()

app = FastAPI(title="API - Influx Data", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "ok"}

# Routers
app.include_router(animals_router, prefix="/api")
app.include_router(collar_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
