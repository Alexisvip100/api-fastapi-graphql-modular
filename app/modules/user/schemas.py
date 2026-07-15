from pydantic import ConfigDict
from uuid import UUID
from pydantic import EmailStr
from pydantic import BaseModel
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool

    model_config = ConfigDict(from_attributes=True)