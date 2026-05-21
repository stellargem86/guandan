"""PostgreSQL 异步数据库连接配置

使用 asyncpg 驱动 + SQLAlchemy 2.0 异步引擎，提供：
- AsyncEngine: 异步数据库引擎
- AsyncSessionLocal: 异步 Session 工厂
- Base: 声明式模型基类
- get_db: FastAPI 依赖注入
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

settings = get_settings()

# 创建异步引擎
_engine_kwargs: dict = {
    "echo": settings.DEBUG,
}
# SQLite 不支持连接池参数
if "sqlite" not in settings.DATABASE_URL:
    _engine_kwargs.update({
        "pool_size": 20,
        "max_overflow": 10,
        "pool_pre_ping": True,
    })

engine = create_async_engine(settings.DATABASE_URL, **_engine_kwargs)

# 异步 Session 工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """声明式模型基类，所有 ORM 模型继承此类"""

    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI 依赖注入 - 获取数据库 Session

    使用 async with 确保 Session 在请求结束后正确关闭。
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
