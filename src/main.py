import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from src.db.database import engine
from src.modules.router import main_router
__ver__ = '0.1'

sentry_sdk.init(
    dsn="https://b538fbcfd6bd4cf12de8abe05edba57b@o4506230928834560.ingest.sentry.io/4506230929883138",
    enable_tracing=True,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    integrations=[
            StarletteIntegration(
                transaction_style="endpoint"
            ),
            FastApiIntegration(
                transaction_style="endpoint"
            ),
        ],
    release=__ver__
)

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


@app.get('/', include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse('/docs')