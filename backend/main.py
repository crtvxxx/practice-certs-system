from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from backend.database import engine
from backend.models import Base
from backend.routers import users, orders

app = FastAPI(title="College Certificates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router)
app.include_router(orders.router)

@app.get("/")
async def root():
    return RedirectResponse(url="/static/index.html")