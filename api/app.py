from fastapi import FastAPI

from core.config import settings

from api.routes.main import api_router


app = FastAPI(openapi_url=f'{settings.API_STR}/openapi.json')

app.include_router(api_router, prefix=settings.API_STR)
