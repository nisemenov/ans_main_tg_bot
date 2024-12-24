from fastapi import APIRouter

from api.routes import notifications


api_router = APIRouter()

api_router.include_router(notifications.router, prefix='/notifications', tags=['notifications'])
