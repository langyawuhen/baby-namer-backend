from datetime import date

from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List, Optional, Annotated

from fastapi_mail import FastMail, MessageType
from pydantic import BaseModel, ValidationError, Field
from sqlalchemy import delete, select, or_

from dependence import get_session, get_mail
from schemas import ResultSchema
from models.user import User
from models import AsyncSession
from aiosmtplib import SMTPResponseException

from schemas.user_schema import UserSchema, UserLoginSchema, UserLoginInSchema

router = APIRouter(prefix="/user", tags=["用户管理"])


# try:
#     class User(BaseModel):
#         id: int
#         name: str
#         date_joined: Optional[date]
#         departments: List[str]
#
#
#     user = User(id=1, name="John", date_joined=date.today(), departments=["技术部", "产品部"])
#     print("user ==>", user.model_dump())
# except ValidationError as e:  # 捕获验证错误 如果是int输入，比如id="1.1",会自动转换为int，但是输入其他字符串会报错
#     print(e.errors)
#
#
# class LoginInfo(BaseModel):
#     username: Annotated[str, Field(..., description="用户名")]
#     password: Annotated[str, Field(..., min_length=6, max_length=20, description="密码")]
#

#
# form_data = {
#     "username": "admin",
#     "password": "123456"
# }
# data = LoginInfo(**form_data)

@router.post("/register", response_model=ResultSchema[UserSchema])
async def register(user_data: UserSchema, session: AsyncSession = Depends(get_session)):
    query = await session.execute(
        select(User).where(or_(User.username == user_data.username, User.email == user_data.email)))
    existing = query.scalars().first()
    print("user_data ==>", user_data)
    try:
        if existing.username == user_data.username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
        if existing.email == user_data.email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已存在")

        async with session.begin():
            user = User(username=user_data.username, password=user_data.password, email=user_data.email)
            session.add(user)
        return {"code": 200, "message": "注册成功", "data": None}
    except Exception as e:
        # await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        # return {"code": 400, "message": f"注册失败,{e}", "data": None}, 400


# @router.post("/login", response_model=ResultSchema[UserLoginSchema])
# async def login(user_data: User, session: AsyncSession = Depends(get_session)):
#     existing_user = session.execute(select(User).where(User.username == user_data.username))
#     print("existing_user ==>", existing_user)
#     return {
#         "username": user_data.username,
#         "password": user_data.password
#     }


@router.delete("/{user_id:int}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    async with session.begin():
        await session.execute(delete(User).where(User.id == user_id))
        return {"code": 200, "message": "删除成功"}, 200


@router.get("/{user_id:int}", response_model=ResultSchema[UserSchema])
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    query = await session.execute(select(User).where(User.id == user_id))
    result = query.scalar()
    if result:
        return {"code": 200, "message": "获取成功", "data": result}
    else:
        return {"code": 404, "message": "用户不存在"}, 404


@router.get("/getUserList", response_model=ResultSchema[List[UserSchema]])
async def get_users(query_params: Optional[str] = Query(None, description="搜索参数"),
                    session: AsyncSession = Depends(get_session)):
    query = await session.execute(select(User).where(User.email.contains(query_params)))
    results = query.scalars().all()
    if query:
        return {"code": 200, "message": "获取成功", "data": results}
    else:
        return {"code": 404, "message": "用户不存在"}, 404


@router.get("/test/sendmail")
async def test_send_mail(email: str, mail: FastMail = Depends(get_mail)):
    message = {
        "subject": "Hello",
        "recipients": [email],
        "body": "这是测试邮件",
        "subtype": MessageType.plain
    }
    try:
        await mail.send_message(message)
    except SMTPResponseException as e:
        print(e)
    return {"code": 200, "message": "发送成功"}
