"""Redis 模块单元测试"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.core.redis import RedisManager


@pytest.fixture
def redis_mgr():
    """创建带 mock client 的 RedisManager"""
    mgr = RedisManager()
    mgr._client = AsyncMock()
    return mgr


class TestRedisManagerLifecycle:
    """连接生命周期测试"""

    def test_client_raises_when_not_connected(self):
        mgr = RedisManager()
        with pytest.raises(RuntimeError, match="Redis not connected"):
            _ = mgr.client

    def test_client_returns_when_connected(self, redis_mgr):
        assert redis_mgr.client is not None

    @pytest.mark.asyncio
    async def test_disconnect_sets_client_none(self, redis_mgr):
        await redis_mgr.disconnect()
        assert redis_mgr._client is None


class TestSessionManagement:
    """Session 管理测试"""

    @pytest.mark.asyncio
    async def test_set_session(self, redis_mgr):
        await redis_mgr.set_session("user123", '{"token": "abc"}', ttl_seconds=3600)
        redis_mgr._client.set.assert_called_once_with(
            "session:user123", '{"token": "abc"}', ex=3600
        )

    @pytest.mark.asyncio
    async def test_get_session(self, redis_mgr):
        redis_mgr._client.get.return_value = '{"token": "abc"}'
        result = await redis_mgr.get_session("user123")
        redis_mgr._client.get.assert_called_once_with("session:user123")
        assert result == '{"token": "abc"}'

    @pytest.mark.asyncio
    async def test_get_session_not_found(self, redis_mgr):
        redis_mgr._client.get.return_value = None
        result = await redis_mgr.get_session("user999")
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_session(self, redis_mgr):
        await redis_mgr.delete_session("user123")
        redis_mgr._client.delete.assert_called_once_with("session:user123")

    @pytest.mark.asyncio
    async def test_refresh_session_ttl(self, redis_mgr):
        redis_mgr._client.expire.return_value = True
        result = await redis_mgr.refresh_session_ttl("user123", ttl_seconds=7200)
        redis_mgr._client.expire.assert_called_once_with("session:user123", 7200)
        assert result is True


class TestGeoOperations:
    """GEO 操作测试"""

    @pytest.mark.asyncio
    async def test_geo_add_merchant(self, redis_mgr):
        redis_mgr._client.geoadd.return_value = 1
        result = await redis_mgr.geo_add_merchant("merchant1", 120.5, 31.2)
        redis_mgr._client.geoadd.assert_called_once_with(
            "geo:merchants", (120.5, 31.2, "merchant1")
        )
        assert result == 1

    @pytest.mark.asyncio
    async def test_geo_add_merchants_batch_empty(self, redis_mgr):
        result = await redis_mgr.geo_add_merchants_batch([])
        assert result == 0
        redis_mgr._client.geoadd.assert_not_called()

    @pytest.mark.asyncio
    async def test_geo_search_merchants(self, redis_mgr):
        redis_mgr._client.geosearch.return_value = [
            ("merchant1", "1.5"),
            ("merchant2", "3.2"),
        ]
        results = await redis_mgr.geo_search_merchants(120.5, 31.2, radius_km=5.0)
        assert len(results) == 2
        assert results[0] == {"member": "merchant1", "dist": 1.5}
        assert results[1] == {"member": "merchant2", "dist": 3.2}

    @pytest.mark.asyncio
    async def test_geo_remove_merchant(self, redis_mgr):
        redis_mgr._client.zrem.return_value = 1
        result = await redis_mgr.geo_remove_merchant("merchant1")
        redis_mgr._client.zrem.assert_called_once_with("geo:merchants", "merchant1")
        assert result == 1

    @pytest.mark.asyncio
    async def test_geo_get_position(self, redis_mgr):
        redis_mgr._client.geopos.return_value = [(120.5, 31.2)]
        result = await redis_mgr.geo_get_position("merchant1")
        assert result == (120.5, 31.2)

    @pytest.mark.asyncio
    async def test_geo_get_position_not_found(self, redis_mgr):
        redis_mgr._client.geopos.return_value = [None]
        result = await redis_mgr.geo_get_position("merchant999")
        assert result is None


class TestRateLimiting:
    """限流测试"""

    @pytest.mark.asyncio
    async def test_first_request_allowed(self, redis_mgr):
        redis_mgr._client.get.return_value = None
        allowed, remaining = await redis_mgr.check_rate_limit("1.2.3.4", "/api/test")
        assert allowed is True
        assert remaining == 59
        redis_mgr._client.set.assert_called_once_with(
            "ratelimit:1.2.3.4:/api/test", 1, ex=60
        )

    @pytest.mark.asyncio
    async def test_within_limit_allowed(self, redis_mgr):
        redis_mgr._client.get.return_value = "30"
        redis_mgr._client.incr.return_value = 31
        allowed, remaining = await redis_mgr.check_rate_limit("1.2.3.4", "/api/test")
        assert allowed is True
        assert remaining == 29

    @pytest.mark.asyncio
    async def test_exceeded_limit_blocked(self, redis_mgr):
        redis_mgr._client.get.return_value = "60"
        allowed, remaining = await redis_mgr.check_rate_limit("1.2.3.4", "/api/test")
        assert allowed is False
        assert remaining == 0


class TestSortedSetRanking:
    """排行榜操作测试"""

    @pytest.mark.asyncio
    async def test_ranking_update_personal(self, redis_mgr):
        await redis_mgr.ranking_update("personal", "user1", 1500.0)
        redis_mgr._client.zadd.assert_called_once_with(
            "ranking:personal", {"user1": 1500.0}
        )

    @pytest.mark.asyncio
    async def test_ranking_update_club(self, redis_mgr):
        await redis_mgr.ranking_update("club", "user1", 1200.0, ranking_id="club1")
        redis_mgr._client.zadd.assert_called_once_with(
            "ranking:club:club1", {"user1": 1200.0}
        )

    @pytest.mark.asyncio
    async def test_ranking_update_region(self, redis_mgr):
        await redis_mgr.ranking_update("region", "user1", 1800.0, ranking_id="南京")
        redis_mgr._client.zadd.assert_called_once_with(
            "ranking:region:南京", {"user1": 1800.0}
        )

    @pytest.mark.asyncio
    async def test_ranking_get_top(self, redis_mgr):
        redis_mgr._client.zrevrange.return_value = [
            ("user1", 1800.0),
            ("user2", 1700.0),
        ]
        results = await redis_mgr.ranking_get_top("personal", start=0, end=1)
        assert len(results) == 2
        assert results[0] == {"member": "user1", "score": 1800.0, "rank": 0}
        assert results[1] == {"member": "user2", "score": 1700.0, "rank": 1}

    @pytest.mark.asyncio
    async def test_ranking_get_rank(self, redis_mgr):
        redis_mgr._client.zrevrank.return_value = 5
        rank = await redis_mgr.ranking_get_rank("personal", "user1")
        assert rank == 5


class TestPostLikes:
    """点赞缓存测试"""

    @pytest.mark.asyncio
    async def test_post_like_add_new(self, redis_mgr):
        redis_mgr._client.sadd.return_value = 1
        result = await redis_mgr.post_like_add("post1", "user1")
        redis_mgr._client.sadd.assert_called_once_with("post:likes:post1", "user1")
        assert result is True

    @pytest.mark.asyncio
    async def test_post_like_add_duplicate(self, redis_mgr):
        redis_mgr._client.sadd.return_value = 0
        result = await redis_mgr.post_like_add("post1", "user1")
        assert result is False

    @pytest.mark.asyncio
    async def test_post_like_remove(self, redis_mgr):
        redis_mgr._client.srem.return_value = 1
        result = await redis_mgr.post_like_remove("post1", "user1")
        redis_mgr._client.srem.assert_called_once_with("post:likes:post1", "user1")
        assert result is True

    @pytest.mark.asyncio
    async def test_post_like_check(self, redis_mgr):
        redis_mgr._client.sismember.return_value = True
        result = await redis_mgr.post_like_check("post1", "user1")
        assert result is True

    @pytest.mark.asyncio
    async def test_post_like_count(self, redis_mgr):
        redis_mgr._client.scard.return_value = 42
        count = await redis_mgr.post_like_count("post1")
        assert count == 42


class TestMatchQueue:
    """组局匹配队列测试"""

    @pytest.mark.asyncio
    async def test_match_queue_add(self, redis_mgr):
        await redis_mgr.match_queue_add("南京", "match1", 1700000000.0)
        redis_mgr._client.zadd.assert_called_once_with(
            "match:queue:南京", {"match1": 1700000000.0}
        )

    @pytest.mark.asyncio
    async def test_match_queue_remove(self, redis_mgr):
        redis_mgr._client.zrem.return_value = 1
        result = await redis_mgr.match_queue_remove("南京", "match1")
        redis_mgr._client.zrem.assert_called_once_with("match:queue:南京", "match1")
        assert result == 1

    @pytest.mark.asyncio
    async def test_match_detail_set(self, redis_mgr):
        data = {"title": "周末约局", "players": "4"}
        await redis_mgr.match_detail_set("match1", data, ttl_seconds=3600)
        redis_mgr._client.hset.assert_called_once_with(
            "match:detail:match1", mapping=data
        )
        redis_mgr._client.expire.assert_called_once_with("match:detail:match1", 3600)

    @pytest.mark.asyncio
    async def test_match_detail_get(self, redis_mgr):
        redis_mgr._client.hgetall.return_value = {"title": "周末约局", "players": "4"}
        result = await redis_mgr.match_detail_get("match1")
        assert result == {"title": "周末约局", "players": "4"}
