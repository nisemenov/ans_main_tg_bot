from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    id: int = Field(serialization_alias='telegram_id')
    first_name: str
    username: str | None = None
    last_name: str | None = None
    is_admin: bool = False
    email: EmailStr | None = None
