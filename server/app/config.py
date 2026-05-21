"""应用配置管理 - 基于 Pydantic Settings，从环境变量读取配置"""

from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置，所有值从环境变量或 .env 文件读取"""

    # 应用基本配置
    APP_NAME: str = "深掼会平台"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # 数据库配置
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/shenguanhui",
        description="PostgreSQL 数据库连接 URL",
    )

    # Redis 配置
    REDIS_URL: str = Field(
        default="redis://localhost:6379/0",
        description="Redis 连接 URL",
    )

    # JWT 配置
    JWT_SECRET: str = Field(
        default="change-me-in-production",
        description="JWT 签名密钥",
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # 微信配置
    WECHAT_APP_ID: str = Field(
        default="",
        description="微信小程序 App ID",
    )
    WECHAT_APP_SECRET: str = Field(
        default="",
        description="微信小程序 App Secret",
    )

    # 微信支付配置
    WECHAT_MCH_ID: str = Field(
        default="",
        description="微信商户号",
    )
    WECHAT_PAY_KEY: str = Field(
        default="",
        description="微信支付 API 密钥",
    )
    WECHAT_PAY_CERT_PATH: str = Field(
        default="",
        description="微信支付证书路径",
    )
    WECHAT_PAY_NOTIFY_URL: str = Field(
        default="",
        description="微信支付回调通知 URL",
    )

    # CORS 配置
    CORS_ORIGINS: list[str] = ["*"]

    # OSS 对象存储配置
    OSS_ENDPOINT: str = Field(default="", description="OSS 存储端点")
    OSS_ACCESS_KEY: str = Field(default="", description="OSS Access Key")
    OSS_SECRET_KEY: str = Field(default="", description="OSS Secret Key")
    OSS_BUCKET: str = Field(default="", description="OSS Bucket 名称")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


@lru_cache
def get_settings() -> Settings:
    """获取配置单例"""
    return Settings()
