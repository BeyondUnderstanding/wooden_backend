from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from src.db.database import engine
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
    print('----------------------------------')
    response = await call_next(request)
    print(engine.pool.status())
    print('----------------------------------')
    return response
