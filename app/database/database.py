# 从 SQLAlchemy 导入异步数据库工具
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# 从 SQLAlchemy 导入数据库模型基类
from sqlalchemy.orm import DeclarativeBase


# 数据库地址
DATABASE_URL = "sqlite+aiosqlite:///./rental_agent.db"

# 创建数据库连接引擎，echo=False 表示不打印 SQL 语句
engine = create_async_engine(DATABASE_URL, echo=False)

# 创建异步数据库会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# 所有数据库表模型都要继承这个 Base
class Base(DeclarativeBase):
    pass

async def init_db():
    from app.database.models import Property

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session