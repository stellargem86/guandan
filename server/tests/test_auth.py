"""认证系统单元测试 - Tasks 2.1, 2.2, 2.3

测试内容：
- JWT Token 签发与解码 (access + refresh)
- Token payload 格式验证
- 密码哈希 (bcrypt cost factor 12)
- Platform ID 生成
- RBAC 角色检查器
"""

import time
from datetime import timedelta
from unittest.mock import AsyncMock, patch

import pytest

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_platform_id,
    get_password_hash,
    verify_password,
    pwd_context,
)
from app.api.deps import RoleChecker


# ─── Task 2.2: JWT Token 签发与刷新 ────────────────────────────────


class TestJWTTokens:
    """JWT Token 签发与验证测试"""

    def test_create_access_token_payload_format(self):
        """Access Token payload 包含必要字段"""
        token = create_access_token(user_id=42, role="merchant")
        payload = decode_token(token)

        assert payload is not None
        assert payload["sub"] == "42"
        assert payload["role"] == "merchant"
        assert payload["type"] == "access"
        assert "jti" in payload
        assert "exp" in payload

    def test_create_refresh_token_payload_format(self):
        """Refresh Token payload 包含必要字段"""
        token = create_refresh_token(user_id=99)
        payload = decode_token(token)

        assert payload is not None
        assert payload["sub"] == "99"
        assert payload["type"] == "refresh"
        assert "jti" in payload
        assert "exp" in payload
        # Refresh token 不应包含 role
        assert "role" not in payload

    def test_access_token_default_expiry_15min(self):
        """Access Token 默认 15 分钟过期"""
        token = create_access_token(user_id=1, role="user")
        payload = decode_token(token)

        # 检查过期时间在 14-16 分钟范围内
        now = time.time()
        exp_delta = payload["exp"] - now
        assert 14 * 60 < exp_delta < 16 * 60

    def test_refresh_token_default_expiry_7days(self):
        """Refresh Token 默认 7 天过期"""
        token = create_refresh_token(user_id=1)
        payload = decode_token(token)

        now = time.time()
        exp_delta = payload["exp"] - now
        # 6.9 到 7.1 天
        assert 6.9 * 86400 < exp_delta < 7.1 * 86400

    def test_custom_expiry(self):
        """支持自定义过期时间"""
        token = create_access_token(
            user_id=1, role="user", expires_delta=timedelta(hours=1)
        )
        payload = decode_token(token)

        now = time.time()
        exp_delta = payload["exp"] - now
        assert 59 * 60 < exp_delta < 61 * 60

    def test_decode_invalid_token_returns_none(self):
        """无效 Token 解码返回 None"""
        assert decode_token("invalid.token.here") is None

    def test_decode_tampered_token_returns_none(self):
        """篡改后的 Token 解码返回 None"""
        token = create_access_token(user_id=1, role="user")
        # 篡改 token
        tampered = token[:-5] + "xxxxx"
        assert decode_token(tampered) is None

    def test_each_token_has_unique_jti(self):
        """每次生成的 Token 都有唯一 JTI"""
        token1 = create_access_token(user_id=1, role="user")
        token2 = create_access_token(user_id=1, role="user")

        payload1 = decode_token(token1)
        payload2 = decode_token(token2)

        assert payload1["jti"] != payload2["jti"]

    def test_user_id_stored_as_string(self):
        """user_id 在 Token 中以字符串存储"""
        token = create_access_token(user_id=123, role="admin")
        payload = decode_token(token)
        assert isinstance(payload["sub"], str)
        assert payload["sub"] == "123"


# ─── Task 2.2: 密码哈希 ────────────────────────────────────────────


class TestPasswordHashing:
    """密码哈希测试"""

    def test_bcrypt_cost_factor_12(self):
        """bcrypt 使用 cost factor 12"""
        # passlib 配置中 rounds=12
        config = pwd_context.to_dict()
        assert config.get("bcrypt__rounds") == 12

    def test_hash_and_verify(self):
        """密码哈希与验证"""
        password = "test_password_123"
        hashed = get_password_hash(password)

        assert verify_password(password, hashed)
        assert not verify_password("wrong_password", hashed)

    def test_hash_is_different_each_time(self):
        """相同密码每次哈希结果不同（随机 salt）"""
        password = "same_password"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2


# ─── Task 2.1: Platform ID 生成 ────────────────────────────────────


class TestPlatformId:
    """Platform ID 生成测试"""

    def test_platform_id_length_16(self):
        """Platform ID 长度为 16 位"""
        pid = generate_platform_id()
        assert len(pid) == 16

    def test_platform_id_is_hex(self):
        """Platform ID 是十六进制字符串"""
        pid = generate_platform_id()
        # 尝试转为 int（十六进制），不抛异常说明是合法 hex
        int(pid, 16)

    def test_platform_id_unique(self):
        """每次生成的 Platform ID 不同"""
        ids = {generate_platform_id() for _ in range(100)}
        assert len(ids) == 100


# ─── Task 2.3: RBAC 权限检查器 ────────────────────────────────────


class TestRBACRoleChecker:
    """RBAC 角色检查器单元测试"""

    def test_role_checker_init(self):
        """RoleChecker 初始化存储允许角色"""
        checker = RoleChecker(["merchant", "admin"])
        assert checker.allowed_roles == ["merchant", "admin"]

    @pytest.mark.asyncio
    async def test_admin_bypasses_all_role_checks(self):
        """Admin 角色通过所有权限检查"""
        checker = RoleChecker(["merchant"])

        # Mock admin user
        mock_user = AsyncMock()
        mock_user.role = "admin"

        result = await checker(current_user=mock_user)
        assert result == mock_user

    @pytest.mark.asyncio
    async def test_allowed_role_passes(self):
        """允许的角色通过检查"""
        checker = RoleChecker(["merchant", "admin"])

        mock_user = AsyncMock()
        mock_user.role = "merchant"

        result = await checker(current_user=mock_user)
        assert result == mock_user

    @pytest.mark.asyncio
    async def test_disallowed_role_raises_403(self):
        """不允许的角色返回 403"""
        from fastapi import HTTPException

        checker = RoleChecker(["admin"])

        mock_user = AsyncMock()
        mock_user.role = "user"

        with pytest.raises(HTTPException) as exc_info:
            await checker(current_user=mock_user)

        assert exc_info.value.status_code == 403

    @pytest.mark.asyncio
    async def test_organizer_cannot_access_merchant_endpoint(self):
        """Organizer 不能访问 merchant 接口"""
        from fastapi import HTTPException

        checker = RoleChecker(["merchant", "admin"])

        mock_user = AsyncMock()
        mock_user.role = "organizer"

        with pytest.raises(HTTPException) as exc_info:
            await checker(current_user=mock_user)

        assert exc_info.value.status_code == 403
