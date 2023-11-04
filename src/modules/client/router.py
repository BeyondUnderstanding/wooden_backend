from fastapi import APIRouter
from .games.router import client_games
from .basket.router import basket

client = APIRouter(prefix='/client')
client.include_router(client_games)
client.include_router(basket)