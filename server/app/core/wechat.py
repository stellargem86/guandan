"""微信 SDK 封装 - OAuth 登录、支付、分账"""

from typing import Optional

import httpx

from app.config import get_settings

settings = get_settings()

# 微信 API 端点
WECHAT_CODE2SESSION_URL = "https://api.weixin.qq.com/sns/jscode2session"
WECHAT_UNIFIED_ORDER_URL = "https://api.mch.weixin.qq.com/v3/pay/transactions/jsapi"


class WeChatError(Exception):
    """微信 API 调用异常"""

    def __init__(self, errcode: int, errmsg: str):
        self.errcode = errcode
        self.errmsg = errmsg
        super().__init__(f"WeChat API error {errcode}: {errmsg}")


class WeChatSDK:
    """微信 SDK 封装类"""

    def __init__(self):
        self.app_id = settings.WECHAT_APP_ID
        self.app_secret = settings.WECHAT_APP_SECRET
        self.mch_id = settings.WECHAT_MCH_ID

    async def code2session(self, code: str) -> dict:
        """通过 code 换取 session_key 和 openid

        调用微信 jscode2session 接口，返回:
        - openid: 用户唯一标识
        - session_key: 会话密钥
        - unionid: 联合 ID（可选，需绑定开放平台）

        Args:
            code: 微信小程序前端 wx.login() 获取的临时登录凭证

        Returns:
            {"openid": str, "session_key": str, "unionid": str | None}

        Raises:
            WeChatError: 微信 API 返回错误码时抛出
        """
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                WECHAT_CODE2SESSION_URL,
                params={
                    "appid": self.app_id,
                    "secret": self.app_secret,
                    "js_code": code,
                    "grant_type": "authorization_code",
                },
            )
            data = resp.json()

        # 微信返回错误码时抛出异常
        if "errcode" in data and data["errcode"] != 0:
            raise WeChatError(
                errcode=data.get("errcode", -1),
                errmsg=data.get("errmsg", "Unknown error"),
            )

        return {
            "openid": data["openid"],
            "session_key": data["session_key"],
            "unionid": data.get("unionid"),
        }

    async def get_user_profile(self, openid: str) -> Optional[dict]:
        """获取微信用户基本信息（小程序场景下信息有限）

        注意：微信小程序不再支持通过后端获取用户头像和昵称，
        需要前端通过 getUserProfile 接口获取后传给后端。

        Args:
            openid: 用户 OpenID

        Returns:
            用户信息字典（如果可用）
        """
        # 微信小程序场景下，用户信息由前端获取后传递
        # 这里仅返回 openid 作为标识
        return {"openid": openid}

    async def create_prepay_order(self, order_data: dict) -> dict:
        """创建微信支付预付单"""
        # TODO: Task 4.1 完整实现
        raise NotImplementedError("WeChat pay not implemented yet")

    async def verify_payment_callback(self, headers: dict, body: bytes) -> dict:
        """验证支付回调签名"""
        # TODO: Task 4.3 完整实现
        raise NotImplementedError("Payment callback verification not implemented yet")


# 全局 SDK 实例
wechat_sdk = WeChatSDK()
