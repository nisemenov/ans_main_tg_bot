from fastapi import APIRouter, HTTPException, status

from api.deps import session_dep
from api.crud import create_notification

from core.schemas import NotificationBase


router = APIRouter()

@router.post('', status_code=status.HTTP_201_CREATED)
async def create(data: NotificationBase, session: session_dep):
    return await create_notification(data=data, session=session)
