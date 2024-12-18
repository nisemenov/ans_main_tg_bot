from __future__ import annotations

from typing import TYPE_CHECKING

import asyncpg

from config import settings

if TYPE_CHECKING:
    from asyncpg import Connection


USERS_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        id integer PRIMARY KEY,
        telegram_id integer UNIQUE NOT NULL,
        username text,
        first_name text,
        last_name text,
        registered_at timestamp DEFAULT NOW(),
        is_admin boolean DEFAULT FALSE
    );
    '''

async def check_db():
    con: Connection = await asyncpg.connect(settings.SQLALCHEMY_CREATE_DATABASE_URI)
    
    db = await con.fetchval(
        'SELECT 1 FROM pg_database WHERE datname = $1',
        settings.POSTGRES_DB
    )
    if not db:
        await con.execute(f'CREATE DATABASE "{settings.POSTGRES_DB}"')    
    
    await con.close()


async def check_table():
    await check_db()

    con: Connection = await asyncpg.connect(settings.SQLALCHEMY_DATABASE_URI)

    await con.execute(USERS_TABLE)
    await con.close()
