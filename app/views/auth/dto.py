from pydantic import BaseModel


class UserWithRoleDto(BaseModel):
    user_id: int
    role: str
