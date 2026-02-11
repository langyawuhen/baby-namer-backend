from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config.setting import settings

DB_URL = settings.DB_URL
engine = create_async_engine(
    DB_URL,
    echo=True,  # 打印sql
    pool_size=10,  # 连接池大小
    pool_timeout=10,  # 连接池等待超时时间
    max_overflow=20,  # 连接池溢出时，最多允许多少个连接
    pool_recycle=3600,  # 连接池中连接空闲时间超过多少秒，就回收,默认为-1，表示永不回收
    pool_pre_ping=True,  # 创建连接时，执行ping命令，检查连接是否正常
)

AsyncSessionFactory = sessionmaker(
    bind=engine,  # 绑定引擎
    class_=AsyncSession,  # 指定session类
    autoflush=True,  # 自动提交
    expire_on_commit=False  # 提交时，不刷新缓存,默认为True
)


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",  # 索引
        "uq": "uq_%(table_name)s_%(column_0_name)s",  # 唯一索引
        "ck": "ck_%(table_name)s_%(constraint_name)s",  # 检查约束
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # 外键
        "pk": "pk_%(table_name)s"  # 主键
    })


from . import user
from . import article
