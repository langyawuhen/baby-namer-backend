from datetime import datetime
from typing import List

from . import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime
from pwdlib import PasswordHash

# from .article import Article

password_hash = PasswordHash.recommended()


class User(Base):
    """用户表"""
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True)
    _password: Mapped[str] = mapped_column("password",String(200))

    user_extension: Mapped["UserExtension"] = relationship(back_populates="user",
                                                           uselist=False)  # 关联 user_extension uselist 限制一个用户只能有一个用户拓展
    articles: Mapped[List["Article"]] = relationship(back_populates="author")

    def __init__(self, *args, **keywords):  # 重写构造函数 args 是构造函数的参数，keywords 是构造函数的参数字典
        super().__init__(**keywords)
        password = keywords.pop("password")
        if password:
            self.password = password  # 调用setter方法

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password: str):
        self._password = password_hash.hash(raw_password)

    def check_password(self, raw_password: str):
        return password_hash.verify(raw_password, self.password)


class EmailCode(Base):
    __tablename__ = "email_code"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    code: Mapped[str] = mapped_column(String(10))
    create_time: Mapped[datetime] = mapped_column(DateTime)


"""一对一的关系"""


class UserExtension(Base):
    """用户拓展表"""
    __tablename__ = "user_extension"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    university: Mapped[str] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), unique=True)  # unique=True 表示user_id不能重复,一对一关系
    # 同一个模块，可以用User，但是不同模块只能用字符串的"User"建立关联关系
    user: Mapped[User] = relationship(back_populates="user_extension")  # 关联 user