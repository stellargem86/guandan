"""全局依赖注入 - 数据库 Session、Redis 连接等"""

import redis.asyncio as aioredis

from app.core.database import get_db  # noqa: F401
from app.core.redis import redis_manager


async def get_redis() -> aioredis.Redis:
    """获取 Redis 客户端实例 - FastAPI 依赖注入"""
    return redis_manager.client
