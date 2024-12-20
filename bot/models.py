import datetime

import sqlalchemy as sa
from sqlalchemy import BigInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.db import Base


class UserModel(Base):
    __tablename__ = 'users'
    __table_args__ = (UniqueConstraint('telegram_id'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger)
    first_name: Mapped[str]
    username: Mapped[str | None]
    last_name: Mapped[str | None]
    registered_at: Mapped[datetime.datetime] = mapped_column(server_default=sa.func.now())
    is_admin: Mapped[bool] = mapped_column(default=False)
    email: Mapped[str | None]
