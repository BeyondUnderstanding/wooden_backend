from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.modules.router import main_router

app = FastAPI(title='Wooden Games API')
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(main_router)
