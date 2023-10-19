import re
from pydantic import BaseModel, Field, validator

from core.exceptions import UserNotValidEmail



class GetUserListResponseSchema(BaseModel):
    id: int = Field(..., description="ID")
    email: str = Field(..., description="Email")
    username: str = Field(..., description="username")
    password: str = Field(..., description="Password")


    class Config:
        orm_mode = True


class CreateUserRequestSchema(BaseModel):
    email: str = Field(..., description="Email")
    password1: str = Field(..., description="Password1", min_length=6)
    password2: str = Field(..., description="Password2")
    username: str = Field(..., description="username")
    full_name: str = Field(default=None, description="fullname")

    @validator("email")
    def isValidEmail(cls, value: str) -> str:
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if not re.fullmatch(regex, value):
            raise UserNotValidEmail
        return value

class CreateUserResponseSchema(BaseModel):
    email: str = Field(..., description="Email")
    username: str = Field(..., description="username")
    full_name: str = Field(default=None, description="fullname")

    class Config:
        orm_mode = True


class LoginResponseSchema(BaseModel):
    token: str = Field(..., description="Access Token")
    refresh_token: str = Field(..., description="Refresh token")
