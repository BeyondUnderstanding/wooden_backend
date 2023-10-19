from fastapi import FastAPI
from modules.router import main_router

app = FastAPI(title='Wooden Games API')


app.include_router(main_router)

