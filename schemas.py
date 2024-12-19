from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    id: int = Field(serialization_alias='telegram_id')
    username: str
    first_name: str | None
    last_name: str | None
    is_admin: bool = False
    email: EmailStr | None = None
