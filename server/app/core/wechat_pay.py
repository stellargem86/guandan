"""微信支付 SDK 封装 - 统一下单、签名验证、回调处理、退款、分账

提供 WeChatPayClient 类封装所有微信支付相关操作：
- JSAPI 统一下单 (create_jsapi_order)
- 支付回调签名验证 (verify_callback_signature)
- 前端支付参数生成 (generate_payment_params)
- 退款 (create_refund)
- 分账 (create_profit_sharing)

所有金额单位内部使用 分(cents)，调用方需自行转换。
"""

import hashlib
import hmac
import logging
import time
import uuid
from typing import Any
from xml.etree import ElementTree

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)

# 微信支付 API 端点
UNIFIED_ORDER_URL = "https://api.mch.weixin.qq.com/pay/unifiedorder"
REFUND_URL = "https://api.mch.weixin.qq.com/secapi/pay/refund"
PROFIT_SHARING_URL = "https://api.mch.weixin.qq.com/secapi/pay/profitsharing"


class WeChatPayError(Exception):
    """微信支付异常"""

    def __init__(self, message: str, code: str = "", detail: str = ""):
        self.message = message
        self.code = code
        self.detail = detail
        super().__init__(self.message)


class WeChatPayClient:
    """微信支付客户端

    封装微信支付 JSAPI 下单、签名验证、回调处理、退款及分账操作。
    通过 get_wechat_pay_client() 依赖注入获取单例实例。
    """

    def __init__(
        self,
        mch_id: str,
        api_key: str,
        app_id: str,
        notify_url: str,
    ):
        """初始化微信支付客户端

        Args:
            mch_id: 微信商户号
            api_key: 微信支付 API 密钥
            app_id: 微信小程序 App ID
            notify_url: 支付结果通知回调 URL
        """
        self.mch_id = mch_id
        self.api_key = api_key
        self.app_id = app_id
        self.notify_url = notify_url

    # ─── 公开方法 ──────────────────────────────────────────────────

    async def create_jsapi_order(
        self,
        order_no: str,
        amount_cents: int,
        description: str,
        openid: str,
    ) -> dict[str, Any]:
        """JSAPI 统一下单

        调用微信支付统一下单接口，获取 prepay_id 并生成前端支付参数。

        Args:
            order_no: 商户订单号（业务唯一）
            amount_cents: 支付金额，单位：分
            description: 商品描述
            openid: 用户微信 openid

        Returns:
            包含 prepay_id 和前端支付参数的字典:
            {
                "prepay_id": "wx...",
                "payment_params": {
                    "timeStamp": "...",
                    "nonceStr": "...",
                    "package": "prepay_id=wx...",
                    "signType": "MD5",
                    "paySign": "..."
                }
            }

        Raises:
            WeChatPayError: 下单失败时抛出
        """
        params = {
            "appid": self.app_id,
            "mch_id": self.mch_id,
            "nonce_str": self._generate_nonce_str(),
            "body": description,
            "out_trade_no": order_no,
            "total_fee": str(amount_cents),
            "spbill_create_ip": "127.0.0.1",
            "notify_url": self.notify_url,
            "trade_type": "JSAPI",
            "openid": openid,
        }

        # 生成签名
        params["sign"] = self._generate_sign(params, self.api_key)

        # 转 XML 发送请求
        xml_data = self._dict_to_xml(params)
        logger.info("微信支付统一下单: order_no=%s, amount=%d分", order_no, amount_cents)

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                UNIFIED_ORDER_URL,
                content=xml_data.encode("utf-8"),
                headers={"Content-Type": "application/xml"},
            )

        # 解析响应
        result = self._xml_to_dict(response.text)

        if result.get("return_code") != "SUCCESS":
            error_msg = result.get("return_msg", "Unknown error")
            logger.error("微信支付统一下单通信失败: %s", error_msg)
            raise WeChatPayError(
                message=f"统一下单通信失败: {error_msg}",
                code="COMMUNICATION_ERROR",
                detail=error_msg,
            )

        if result.get("result_code") != "SUCCESS":
            err_code = result.get("err_code", "")
            err_desc = result.get("err_code_des", "")
            logger.error("微信支付统一下单业务失败: code=%s, desc=%s", err_code, err_desc)
            raise WeChatPayError(
                message=f"统一下单失败: {err_desc}",
                code=err_code,
                detail=err_desc,
            )

        prepay_id = result.get("prepay_id", "")
        if not prepay_id:
            raise WeChatPayError(
                message="统一下单返回结果缺少 prepay_id",
                code="MISSING_PREPAY_ID",
            )

        # 生成前端支付参数
        payment_params = self.generate_payment_params(prepay_id)

        logger.info("微信支付统一下单成功: order_no=%s, prepay_id=%s", order_no, prepay_id)
        return {
            "prepay_id": prepay_id,
            "payment_params": payment_params,
        }

    def verify_callback_signature(self, data: dict[str, str], signature: str) -> bool:
        """验证微信支付回调签名

        Args:
            data: 回调通知中的参数字典（不含 sign 字段）
            signature: 回调中的 sign 值

        Returns:
            签名验证是否通过
        """
        expected_sign = self._generate_sign(data, self.api_key)
        is_valid = hmac.compare_digest(expected_sign.upper(), signature.upper())
        if not is_valid:
            logger.warning("微信支付回调签名验证失败")
        return is_valid

    def generate_payment_params(self, prepay_id: str) -> dict[str, str]:
        """生成前端调起支付所需参数

        Args:
            prepay_id: 预支付交易会话标识

        Returns:
            前端支付参数字典:
            {
                "timeStamp": "...",
                "nonceStr": "...",
                "package": "prepay_id=...",
                "signType": "MD5",
                "paySign": "..."
            }
        """
        params = {
            "appId": self.app_id,
            "timeStamp": str(int(time.time())),
            "nonceStr": self._generate_nonce_str(),
            "package": f"prepay_id={prepay_id}",
            "signType": "MD5",
        }

        params["paySign"] = self._generate_sign(params, self.api_key)

        # 前端不需要 appId 参数（小程序已有上下文）
        return {
            "timeStamp": params["timeStamp"],
            "nonceStr": params["nonceStr"],
            "package": params["package"],
            "signType": params["signType"],
            "paySign": params["paySign"],
        }

    async def create_refund(
        self,
        order_no: str,
        refund_no: str,
        total_amount: int,
        refund_amount: int,
        reason: str = "",
    ) -> dict[str, Any]:
        """申请退款

        Args:
            order_no: 原商户订单号
            refund_no: 退款单号（商户自定义，唯一）
            total_amount: 原订单总金额，单位：分
            refund_amount: 退款金额，单位：分
            reason: 退款原因

        Returns:
            退款结果字典

        Raises:
            WeChatPayError: 退款失败时抛出
        """
        params: dict[str, str] = {
            "appid": self.app_id,
            "mch_id": self.mch_id,
            "nonce_str": self._generate_nonce_str(),
            "out_trade_no": order_no,
            "out_refund_no": refund_no,
            "total_fee": str(total_amount),
            "refund_fee": str(refund_amount),
        }
        if reason:
            params["refund_desc"] = reason

        params["sign"] = self._generate_sign(params, self.api_key)
        xml_data = self._dict_to_xml(params)

        logger.info(
            "微信支付退款: order_no=%s, refund_no=%s, amount=%d分",
            order_no,
            refund_no,
            refund_amount,
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                REFUND_URL,
                content=xml_data.encode("utf-8"),
                headers={"Content-Type": "application/xml"},
            )

        result = self._xml_to_dict(response.text)

        if result.get("return_code") != "SUCCESS":
            error_msg = result.get("return_msg", "Unknown error")
            logger.error("微信退款通信失败: %s", error_msg)
            raise WeChatPayError(
                message=f"退款通信失败: {error_msg}",
                code="COMMUNICATION_ERROR",
                detail=error_msg,
            )

        if result.get("result_code") != "SUCCESS":
            err_code = result.get("err_code", "")
            err_desc = result.get("err_code_des", "")
            logger.error("微信退款业务失败: code=%s, desc=%s", err_code, err_desc)
            raise WeChatPayError(
                message=f"退款失败: {err_desc}",
                code=err_code,
                detail=err_desc,
            )

        logger.info("微信退款成功: refund_no=%s", refund_no)
        return {
            "refund_id": result.get("refund_id", ""),
            "out_refund_no": result.get("out_refund_no", refund_no),
            "refund_fee": int(result.get("refund_fee", refund_amount)),
        }

    async def create_profit_sharing(
        self,
        transaction_id: str,
        receivers: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """请求分账

        调用微信支付分账 API 将资金分给指定接收方。

        Args:
            transaction_id: 微信支付订单号（微信返回的 transaction_id）
            receivers: 分账接收方列表，每项包含:
                - type: 接收方类型 (MERCHANT_ID / PERSONAL_OPENID)
                - account: 接收方账号
                - amount: 分账金额（分）
                - description: 分账描述

        Returns:
            分账结果字典

        Raises:
            WeChatPayError: 分账失败时抛出
        """
        import json

        params: dict[str, str] = {
            "appid": self.app_id,
            "mch_id": self.mch_id,
            "nonce_str": self._generate_nonce_str(),
            "transaction_id": transaction_id,
            "out_order_no": self._generate_nonce_str(),
            "receivers": json.dumps(receivers, ensure_ascii=False),
        }

        params["sign"] = self._generate_sign(params, self.api_key, sign_type="HMAC-SHA256")
        xml_data = self._dict_to_xml(params)

        logger.info("微信分账请求: transaction_id=%s, receivers=%d", transaction_id, len(receivers))

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                PROFIT_SHARING_URL,
                content=xml_data.encode("utf-8"),
                headers={"Content-Type": "application/xml"},
            )

        result = self._xml_to_dict(response.text)

        if result.get("return_code") != "SUCCESS":
            error_msg = result.get("return_msg", "Unknown error")
            logger.error("微信分账通信失败: %s", error_msg)
            raise WeChatPayError(
                message=f"分账通信失败: {error_msg}",
                code="COMMUNICATION_ERROR",
                detail=error_msg,
            )

        if result.get("result_code") != "SUCCESS":
            err_code = result.get("err_code", "")
            err_desc = result.get("err_code_des", "")
            logger.error("微信分账业务失败: code=%s, desc=%s", err_code, err_desc)
            raise WeChatPayError(
                message=f"分账失败: {err_desc}",
                code=err_code,
                detail=err_desc,
            )

        logger.info("微信分账成功: transaction_id=%s", transaction_id)
        return {
            "order_id": result.get("order_id", ""),
            "out_order_no": result.get("out_order_no", ""),
            "transaction_id": transaction_id,
        }

    # ─── 辅助方法 ──────────────────────────────────────────────────

    @staticmethod
    def _generate_nonce_str() -> str:
        """生成随机字符串

        Returns:
            32 位随机字符串 (UUID4 去除连字符)
        """
        return uuid.uuid4().hex

    @staticmethod
    def _generate_sign(
        params: dict[str, str], key: str, sign_type: str = "MD5"
    ) -> str:
        """生成微信支付签名

        按照微信支付签名算法：
        1. 参数按 key ASCII 排序
        2. 拼接为 key=value&key=value 形式
        3. 末尾追加 &key=<API_KEY>
        4. MD5 或 HMAC-SHA256 计算哈希
        5. 转大写

        Args:
            params: 待签名参数（不含 sign 字段）
            key: API 密钥
            sign_type: 签名类型，MD5 或 HMAC-SHA256

        Returns:
            签名字符串（大写）
        """
        # 过滤空值和 sign 字段，按 key 排序
        filtered = {
            k: v for k, v in params.items() if v and k != "sign"
        }
        sorted_keys = sorted(filtered.keys())
        sign_str = "&".join(f"{k}={filtered[k]}" for k in sorted_keys)
        sign_str += f"&key={key}"

        if sign_type == "HMAC-SHA256":
            signature = hmac.HMAC(
                key.encode("utf-8"),
                sign_str.encode("utf-8"),
                hashlib.sha256,
            ).hexdigest().upper()
        else:
            signature = hashlib.md5(sign_str.encode("utf-8")).hexdigest().upper()

        return signature

    @staticmethod
    def _dict_to_xml(data: dict[str, str]) -> str:
        """将字典转换为 XML 字符串

        Args:
            data: 参数字典

        Returns:
            XML 格式字符串
        """
        xml_parts = ["<xml>"]
        for key, value in data.items():
            # CDATA 包裹非数字值
            if str(value).isdigit():
                xml_parts.append(f"<{key}>{value}</{key}>")
            else:
                xml_parts.append(f"<{key}><![CDATA[{value}]]></{key}>")
        xml_parts.append("</xml>")
        return "".join(xml_parts)

    @staticmethod
    def _xml_to_dict(xml_str: str) -> dict[str, str]:
        """将 XML 字符串转换为字典

        Args:
            xml_str: XML 格式字符串

        Returns:
            参数字典
        """
        try:
            root = ElementTree.fromstring(xml_str)
            return {child.tag: (child.text or "") for child in root}
        except ElementTree.ParseError as e:
            logger.error("XML 解析失败: %s", str(e))
            return {}


# ─── 单例实例和依赖注入 ─────────────────────────────────────────────

_wechat_pay_client: WeChatPayClient | None = None


def get_wechat_pay_client() -> WeChatPayClient:
    """获取微信支付客户端单例（FastAPI 依赖注入）

    Returns:
        WeChatPayClient 实例

    Usage:
        @router.post("/orders")
        async def create_order(
            pay_client: WeChatPayClient = Depends(get_wechat_pay_client)
        ):
            ...
    """
    global _wechat_pay_client
    if _wechat_pay_client is None:
        settings = get_settings()
        _wechat_pay_client = WeChatPayClient(
            mch_id=settings.WECHAT_MCH_ID,
            api_key=settings.WECHAT_PAY_KEY,
            app_id=settings.WECHAT_APP_ID,
            notify_url=settings.WECHAT_PAY_NOTIFY_URL,
        )
    return _wechat_pay_client
