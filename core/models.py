from __future__ import annotations

import datetime

import sqlalchemy as sa
from sqlalchemy import BigInteger, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy


class Base(DeclarativeBase):
    pass


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
    
    user_service_associations: Mapped[list[UserServiceAssociation]] = relationship()

    services: AssociationProxy[list[ServiceModel]] = association_proxy(
        'user_service_associations',
        'service',
        creator=lambda service_obj: UserServiceAssociation(service=service_obj)
    )

    def __repr__(self):
        return f'<User {self.first_name} / {self.id}>'


class ServiceModel(Base):
    __tablename__ = 'services'
    __table_args__ = (UniqueConstraint('title'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]

    notifications: Mapped[list[NotificationModel]] = relationship(
        back_populates='service'
    )

    def __repr__(self):
        return f'<Service {self.title} / {self.id}>'
    

class NotificationModel(Base):
    __tablename__ = 'notifications'

    id: Mapped[int] = mapped_column(primary_key=True)
    message: Mapped[str]
    
    service: Mapped[ServiceModel] = relationship(back_populates='notifications')
    service_id: Mapped[int] = mapped_column(ForeignKey('services.id'))

    def __repr__(self):
        return f'<Notification {self.id}>'


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
    service: Mapped[ServiceModel] = relationship()
