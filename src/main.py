from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from db.database import engine
from src.modules.router import main_router

app = FastAPI(title='Wooden Games API')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(main_router)


@app.middleware('http')
async def pool_monitoring(request: Request, call_next):
    try:
        print(engine.pool.status())
    except Exception as e:
        print(e)
    response = await call_next(request)
    return response
