"""Redis 连接管理 - Session、GEO、限流、排行榜、点赞缓存

提供 RedisManager 类封装所有 Redis 操作，包括：
- 连接池生命周期管理 (connect/disconnect)
- Session 管理 (set/get/delete, TTL 支持)
- GEO 操作 (GEOADD, GEOSEARCH for LBS)
- 限流 (滑动窗口计数器 + EXPIRE)
- Sorted Set 操作 (排行榜)
- Set 操作 (帖子点赞缓存)

Key patterns:
- geo:merchants (GEO)
- ranking:personal, ranking:club:{id}, ranking:region:{name} (Sorted Set)
- match:queue:{region}, match:detail:{id} (Sorted Set + Hash)
- session:{user_id} (String)
- ratelimit:{ip}:{endpoint} (String + EXPIRE)
- post:likes:{post_id} (Set)
"""

from typing import Optional

import redis.asyncio as aioredis

from app.config import get_settings


class RedisManager:
    """Redis 连接管理器，封装所有 Redis 操作"""

    def __init__(self) -> None:
        self._client: Optional[aioredis.Redis] = None

    @property
    def client(self) -> aioredis.Redis:
        """获取 Redis 客户端，未连接时抛出异常"""
        if self._client is None:
            raise RuntimeError("Redis not connected. Call connect() first.")
        return self._client

    @property
    def is_connected(self) -> bool:
        """检查 Redis 是否已连接"""
        return self._client is not None

    async def connect(self) -> None:
        """初始化 Redis 连接池"""
        settings = get_settings()
        self._client = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=20,
        )
        # 验证连接
        await self._client.ping()

    async def disconnect(self) -> None:
        """关闭 Redis 连接池"""
        if self._client:
            await self._client.close()
            self._client = None

    # ─── Session 管理 ───────────────────────────────────────────────

    async def set_session(
        self, user_id: str, data: str, ttl_seconds: int = 86400
    ) -> None:
        """设置用户 Session

        Args:
            user_id: 用户 ID
            data: Session 数据 (JSON 字符串)
            ttl_seconds: 过期时间，默认 24 小时
        """
        key = f"session:{user_id}"
        await self.client.set(key, data, ex=ttl_seconds)

    async def get_session(self, user_id: str) -> Optional[str]:
        """获取用户 Session

        Args:
            user_id: 用户 ID

        Returns:
            Session 数据字符串，不存在返回 None
        """
        key = f"session:{user_id}"
        return await self.client.get(key)

    async def delete_session(self, user_id: str) -> None:
        """删除用户 Session

        Args:
            user_id: 用户 ID
        """
        key = f"session:{user_id}"
        await self.client.delete(key)

    async def refresh_session_ttl(
        self, user_id: str, ttl_seconds: int = 86400
    ) -> bool:
        """刷新 Session TTL

        Args:
            user_id: 用户 ID
            ttl_seconds: 新的过期时间

        Returns:
            True 如果 key 存在并成功设置 TTL
        """
        key = f"session:{user_id}"
        return await self.client.expire(key, ttl_seconds)

    # ─── GEO 操作 (LBS) ────────────────────────────────────────────

    async def geo_add_merchant(
        self, merchant_id: str, longitude: float, latitude: float
    ) -> int:
        """添加商户地理位置

        Args:
            merchant_id: 商户 ID
            longitude: 经度
            latitude: 纬度

        Returns:
            新添加的元素数量
        """
        return await self.client.geoadd(
            "geo:merchants", (longitude, latitude, merchant_id)
        )

    async def geo_add_merchants_batch(
        self, locations: list[tuple[str, float, float]]
    ) -> int:
        """批量添加商户地理位置

        Args:
            locations: [(merchant_id, longitude, latitude), ...]

        Returns:
            新添加的元素数量
        """
        if not locations:
            return 0
        members = [(lng, lat, mid) for mid, lng, lat in locations]
        return await self.client.geoadd("geo:merchants", *members)

    async def geo_search_merchants(
        self,
        longitude: float,
        latitude: float,
        radius_km: float = 5.0,
        count: int = 50,
        sort_asc: bool = True,
    ) -> list[dict]:
        """搜索附近商户

        Args:
            longitude: 中心经度
            latitude: 中心纬度
            radius_km: 搜索半径 (km)
            count: 最大返回数量
            sort_asc: 是否按距离升序排列

        Returns:
            [{"member": merchant_id, "dist": distance_km}, ...]
        """
        results = await self.client.geosearch(
            name="geo:merchants",
            longitude=longitude,
            latitude=latitude,
            radius=radius_km,
            unit="km",
            count=count,
            sort="ASC" if sort_asc else "DESC",
            withdist=True,
        )
        # geosearch 返回 [(member, distance), ...] 当 withdist=True
        return [
            {"member": item[0], "dist": float(item[1])}
            for item in results
        ]

    async def geo_remove_merchant(self, merchant_id: str) -> int:
        """移除商户地理位置

        Args:
            merchant_id: 商户 ID

        Returns:
            移除的元素数量
        """
        return await self.client.zrem("geo:merchants", merchant_id)

    async def geo_get_position(
        self, merchant_id: str
    ) -> Optional[tuple[float, float]]:
        """获取商户位置坐标

        Args:
            merchant_id: 商户 ID

        Returns:
            (longitude, latitude) 或 None
        """
        positions = await self.client.geopos("geo:merchants", merchant_id)
        if positions and positions[0]:
            return positions[0]
        return None

    # ─── 限流 (Rate Limiting) ──────────────────────────────────────

    async def check_rate_limit(
        self, identifier: str, endpoint: str, max_requests: int = 60, window_seconds: int = 60
    ) -> tuple[bool, int]:
        """检查限流（滑动窗口计数器）

        Args:
            identifier: 标识符 (IP 或 user_id)
            endpoint: 接口路径
            max_requests: 窗口内最大请求数
            window_seconds: 窗口时间 (秒)

        Returns:
            (is_allowed, remaining_requests)
        """
        key = f"ratelimit:{identifier}:{endpoint}"
        current = await self.client.get(key)

        if current is None:
            # 第一次请求，初始化计数器
            await self.client.set(key, 1, ex=window_seconds)
            return True, max_requests - 1

        count = int(current)
        if count >= max_requests:
            return False, 0

        # 递增计数器
        new_count = await self.client.incr(key)
        return True, max(0, max_requests - new_count)

    async def get_rate_limit_ttl(self, identifier: str, endpoint: str) -> int:
        """获取限流 key 剩余过期时间

        Args:
            identifier: 标识符
            endpoint: 接口路径

        Returns:
            剩余秒数，-1 表示无过期，-2 表示 key 不存在
        """
        key = f"ratelimit:{identifier}:{endpoint}"
        return await self.client.ttl(key)

    # ─── Sorted Set 操作 (排行榜) ──────────────────────────────────

    async def ranking_update(
        self, ranking_type: str, member: str, score: float, ranking_id: str = ""
    ) -> None:
        """更新排行榜分数

        Args:
            ranking_type: 排行类型 (personal, club, region)
            member: 成员标识
            score: 分数
            ranking_id: 子标识 (俱乐部 ID 或地区名)
        """
        if ranking_id:
            key = f"ranking:{ranking_type}:{ranking_id}"
        else:
            key = f"ranking:{ranking_type}"
        await self.client.zadd(key, {member: score})

    async def ranking_get_top(
        self, ranking_type: str, start: int = 0, end: int = 49, ranking_id: str = ""
    ) -> list[dict]:
        """获取排行榜 Top N

        Args:
            ranking_type: 排行类型
            start: 起始排名 (0-indexed)
            end: 结束排名 (inclusive)
            ranking_id: 子标识

        Returns:
            [{"member": id, "score": score, "rank": rank}, ...]
        """
        if ranking_id:
            key = f"ranking:{ranking_type}:{ranking_id}"
        else:
            key = f"ranking:{ranking_type}"
        results = await self.client.zrevrange(key, start, end, withscores=True)
        return [
            {"member": member, "score": score, "rank": start + i}
            for i, (member, score) in enumerate(results)
        ]

    async def ranking_get_rank(
        self, ranking_type: str, member: str, ranking_id: str = ""
    ) -> Optional[int]:
        """获取成员排名

        Args:
            ranking_type: 排行类型
            member: 成员标识
            ranking_id: 子标识

        Returns:
            排名 (0-indexed, 降序)，不存在返回 None
        """
        if ranking_id:
            key = f"ranking:{ranking_type}:{ranking_id}"
        else:
            key = f"ranking:{ranking_type}"
        return await self.client.zrevrank(key, member)

    async def ranking_get_score(
        self, ranking_type: str, member: str, ranking_id: str = ""
    ) -> Optional[float]:
        """获取成员分数

        Args:
            ranking_type: 排行类型
            member: 成员标识
            ranking_id: 子标识

        Returns:
            分数，不存在返回 None
        """
        if ranking_id:
            key = f"ranking:{ranking_type}:{ranking_id}"
        else:
            key = f"ranking:{ranking_type}"
        return await self.client.zscore(key, member)

    async def ranking_remove(
        self, ranking_type: str, member: str, ranking_id: str = ""
    ) -> int:
        """移除排行榜成员

        Args:
            ranking_type: 排行类型
            member: 成员标识
            ranking_id: 子标识

        Returns:
            移除的元素数量
        """
        if ranking_id:
            key = f"ranking:{ranking_type}:{ranking_id}"
        else:
            key = f"ranking:{ranking_type}"
        return await self.client.zrem(key, member)

    # ─── Set 操作 (点赞缓存) ───────────────────────────────────────

    async def post_like_add(self, post_id: str, user_id: str) -> bool:
        """添加点赞

        Args:
            post_id: 帖子 ID
            user_id: 用户 ID

        Returns:
            True 如果是新增点赞（之前未点赞）
        """
        key = f"post:likes:{post_id}"
        result = await self.client.sadd(key, user_id)
        return result == 1

    async def post_like_remove(self, post_id: str, user_id: str) -> bool:
        """取消点赞

        Args:
            post_id: 帖子 ID
            user_id: 用户 ID

        Returns:
            True 如果成功取消（之前已点赞）
        """
        key = f"post:likes:{post_id}"
        result = await self.client.srem(key, user_id)
        return result == 1

    async def post_like_check(self, post_id: str, user_id: str) -> bool:
        """检查用户是否已点赞

        Args:
            post_id: 帖子 ID
            user_id: 用户 ID

        Returns:
            True 如果已点赞
        """
        key = f"post:likes:{post_id}"
        return await self.client.sismember(key, user_id)

    async def post_like_count(self, post_id: str) -> int:
        """获取帖子点赞数

        Args:
            post_id: 帖子 ID

        Returns:
            点赞总数
        """
        key = f"post:likes:{post_id}"
        return await self.client.scard(key)

    # ─── 组局匹配队列 ─────────────────────────────────────────────

    async def match_queue_add(
        self, region: str, match_id: str, score: float
    ) -> None:
        """将组局添加到区域匹配队列

        Args:
            region: 地区标识
            match_id: 组局 ID
            score: 排序分数 (可用时间戳)
        """
        key = f"match:queue:{region}"
        await self.client.zadd(key, {match_id: score})

    async def match_queue_remove(self, region: str, match_id: str) -> int:
        """从区域匹配队列移除组局

        Args:
            region: 地区标识
            match_id: 组局 ID

        Returns:
            移除的元素数量
        """
        key = f"match:queue:{region}"
        return await self.client.zrem(key, match_id)

    async def match_queue_list(
        self, region: str, start: int = 0, end: int = 19
    ) -> list[tuple[str, float]]:
        """获取区域匹配队列列表

        Args:
            region: 地区标识
            start: 起始位置
            end: 结束位置

        Returns:
            [(match_id, score), ...]
        """
        key = f"match:queue:{region}"
        return await self.client.zrange(key, start, end, withscores=True)

    async def match_detail_set(
        self, match_id: str, data: dict, ttl_seconds: int = 86400
    ) -> None:
        """存储组局详情

        Args:
            match_id: 组局 ID
            data: 组局详情字典
            ttl_seconds: 过期时间
        """
        key = f"match:detail:{match_id}"
        await self.client.hset(key, mapping=data)
        await self.client.expire(key, ttl_seconds)

    async def match_detail_get(self, match_id: str) -> dict:
        """获取组局详情

        Args:
            match_id: 组局 ID

        Returns:
            组局详情字典
        """
        key = f"match:detail:{match_id}"
        return await self.client.hgetall(key)

    async def match_detail_delete(self, match_id: str) -> int:
        """删除组局详情

        Args:
            match_id: 组局 ID

        Returns:
            删除的 key 数量
        """
        key = f"match:detail:{match_id}"
        return await self.client.delete(key)


# 全局 RedisManager 单例
redis_manager = RedisManager()


async def get_redis() -> aioredis.Redis:
    """FastAPI 依赖注入 - 获取 Redis 客户端实例"""
    return redis_manager.client
