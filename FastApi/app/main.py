from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from app.db import db
from app.core.models.base import BaseModel
from app.routers import user

import logging

@asynccontextmanager
async def lifespan(_fastapi_app: FastAPI):
    logging.info("Connecting to database...")
    await db.connect()
    async with db.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    print("Database connected.")
    yield
    print("Disconnecting database...")
    await db.disconnect()

app = FastAPI(lifespan=lifespan)
app.include_router(user.router)

@app.get("/")
async def read_root():
    return {"Hello": "World", "Service": "LMS API"}

@app.get("/health")
async def health():
    ok = await db.ping()
    return {"status": "ok" if ok else "error"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True)