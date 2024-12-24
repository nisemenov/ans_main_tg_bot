from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from core.config import sqlalchemy_config


session_dep = Annotated[AsyncSession, Depends(sqlalchemy_config.get_session)]
