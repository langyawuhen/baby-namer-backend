from typing import List

from sqlalchemy import String, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base

# from .user import User

"""文章和作者一对多关系"""
"""文章和标签是多对多的关系"""


class Article(Base):
    """文章表"""
    __tablename__ = "article"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)

    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="articles")

    tags: Mapped[List["Tag"]] = relationship("Tag", back_populates="articles",
                                             secondary="article_tag")  # secondary 表示中间表


class Tag(Base):
    """标签表"""
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))

    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("article.id"))
    articles: Mapped["Article"] = relationship("Article", back_populates="tags",
                                              secondary="article_tag")  # secondary 表示中间表


class ArticleTag(Base):
    """文章标签关系表（中间表）"""
    __tablename__ = "article_tag"

    article_id: Mapped[int] = mapped_column(Integer, ForeignKey("article.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey("tag.id"), primary_key=True)
