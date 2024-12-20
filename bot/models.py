import datetime

import sqlalchemy as sa
from sqlalchemy import BigInteger, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy

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
    services: Mapped[list['ServiceModel']] = relationship(

    )

    service_titles: Mapped[list[str]] = association_proxy(
        'services',
        'title'
    )


class ServiceModel(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]


class UserServiceAssociation(Base):
    __tablename__ = 'user_service_associations'
    
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), 
        primary_key=True
    )
    service_id: Mapped[int] = mapped_column(
        ForeignKey('services.id'), 
        primary_key=True
    )
