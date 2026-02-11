from typing import List, Optional, Annotated, Union

from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    # id: int
    username: Annotated[str, Field(..., min_length=1, max_length=20, description="用户名")]
    password: Annotated[str, Field(..., min_length=6, max_length=100, description="密码")]
    email: Annotated[Union[EmailStr, None], Field(default=None, min_length=1, max_length=100, description="邮箱")]


class UsersSchema(BaseModel):
    users: List[UserSchema]


class UserQueryParams(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    # sort_by: Optional[str] = "id"
    # sort_order: Optional[str] = "asc"


class UserLoginSchema(BaseModel):
    username: str
    token: str


class UserLoginInSchema(BaseModel):
    username: str
    password: str
