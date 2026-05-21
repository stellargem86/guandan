"""微信支付 SDK 单元测试"""

import hashlib
import hmac as hmac_module
from unittest.mock import AsyncMock, patch

import pytest

from app.core.wechat_pay import WeChatPayClient, WeChatPayError, get_wechat_pay_client


@pytest.fixture
def pay_client():
    """创建测试用微信支付客户端"""
    return WeChatPayClient(
        mch_id="1234567890",
        api_key="test_api_key_32_chars_long_xxxxx",
        app_id="wx_test_app_id",
        notify_url="https://example.com/api/v1/payments/callback",
    )


class TestGenerateNonceStr:
    """测试随机字符串生成"""

    def test_returns_32_char_string(self, pay_client: WeChatPayClient):
        nonce = pay_client._generate_nonce_str()
        assert len(nonce) == 32
        assert nonce.isalnum()

    def test_generates_unique_values(self, pay_client: WeChatPayClient):
        nonces = {pay_client._generate_nonce_str() for _ in range(100)}
        assert len(nonces) == 100


class TestGenerateSign:
    """测试签名生成"""

    def test_md5_sign_basic(self, pay_client: WeChatPayClient):
        params = {
            "appid": "wx_test_app_id",
            "mch_id": "1234567890",
            "nonce_str": "abc123",
            "body": "测试商品",
        }
        key = "test_api_key_32_chars_long_xxxxx"
        sign = pay_client._generate_sign(params, key)

        # 手动计算预期签名
        sign_str = "appid=wx_test_app_id&body=测试商品&mch_id=1234567890&nonce_str=abc123&key=test_api_key_32_chars_long_xxxxx"
        expected = hashlib.md5(sign_str.encode("utf-8")).hexdigest().upper()
        assert sign == expected

    def test_hmac_sha256_sign(self, pay_client: WeChatPayClient):
        params = {"appid": "wxapp", "mch_id": "123"}
        key = "mykey"
        sign = pay_client._generate_sign(params, key, sign_type="HMAC-SHA256")

        sign_str = "appid=wxapp&mch_id=123&key=mykey"
        expected = hmac_module.HMAC(
            key.encode("utf-8"),
            sign_str.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest().upper()
        assert sign == expected

    def test_excludes_empty_values(self, pay_client: WeChatPayClient):
        params = {"appid": "wx123", "mch_id": "", "body": "test"}
        key = "key123"
        sign = pay_client._generate_sign(params, key)

        # mch_id 为空应被排除
        sign_str = "appid=wx123&body=test&key=key123"
        expected = hashlib.md5(sign_str.encode("utf-8")).hexdigest().upper()
        assert sign == expected

    def test_excludes_sign_field(self, pay_client: WeChatPayClient):
        params = {"appid": "wx123", "sign": "old_sign", "body": "test"}
        key = "key123"
        sign = pay_client._generate_sign(params, key)

        # sign 字段应被排除
        sign_str = "appid=wx123&body=test&key=key123"
        expected = hashlib.md5(sign_str.encode("utf-8")).hexdigest().upper()
        assert sign == expected


class TestDictToXml:
    """测试字典转 XML"""

    def test_basic_conversion(self, pay_client: WeChatPayClient):
        data = {"appid": "wx123", "total_fee": "100"}
        xml = pay_client._dict_to_xml(data)
        assert "<xml>" in xml
        assert "</xml>" in xml
        assert "<appid><![CDATA[wx123]]></appid>" in xml
        assert "<total_fee>100</total_fee>" in xml

    def test_numeric_values_no_cdata(self, pay_client: WeChatPayClient):
        data = {"amount": "19900"}
        xml = pay_client._dict_to_xml(data)
        assert "<amount>19900</amount>" in xml

    def test_string_values_with_cdata(self, pay_client: WeChatPayClient):
        data = {"body": "深掼会-餐饮套餐"}
        xml = pay_client._dict_to_xml(data)
        assert "<body><![CDATA[深掼会-餐饮套餐]]></body>" in xml


class TestXmlToDict:
    """测试 XML 转字典"""

    def test_basic_conversion(self, pay_client: WeChatPayClient):
        xml = "<xml><return_code>SUCCESS</return_code><prepay_id>wx123</prepay_id></xml>"
        result = pay_client._xml_to_dict(xml)
        assert result == {"return_code": "SUCCESS", "prepay_id": "wx123"}

    def test_empty_element(self, pay_client: WeChatPayClient):
        xml = "<xml><code></code></xml>"
        result = pay_client._xml_to_dict(xml)
        assert result == {"code": ""}

    def test_invalid_xml_returns_empty_dict(self, pay_client: WeChatPayClient):
        result = pay_client._xml_to_dict("not valid xml")
        assert result == {}


class TestVerifyCallbackSignature:
    """测试回调签名验证"""

    def test_valid_signature(self, pay_client: WeChatPayClient):
        data = {
            "appid": "wx_test_app_id",
            "mch_id": "1234567890",
            "result_code": "SUCCESS",
            "out_trade_no": "ORDER001",
        }
        # 生成正确签名
        sign = pay_client._generate_sign(data, pay_client.api_key)
        assert pay_client.verify_callback_signature(data, sign) is True

    def test_invalid_signature(self, pay_client: WeChatPayClient):
        data = {"appid": "wx_test_app_id", "mch_id": "1234567890"}
        assert pay_client.verify_callback_signature(data, "INVALID_SIGN") is False

    def test_case_insensitive_comparison(self, pay_client: WeChatPayClient):
        data = {"appid": "wx_test_app_id"}
        sign = pay_client._generate_sign(data, pay_client.api_key)
        assert pay_client.verify_callback_signature(data, sign.lower()) is True


class TestGeneratePaymentParams:
    """测试前端支付参数生成"""

    def test_contains_required_fields(self, pay_client: WeChatPayClient):
        params = pay_client.generate_payment_params("wx_prepay_123")
        assert "timeStamp" in params
        assert "nonceStr" in params
        assert "package" in params
        assert "signType" in params
        assert "paySign" in params

    def test_package_format(self, pay_client: WeChatPayClient):
        params = pay_client.generate_payment_params("wx_prepay_123")
        assert params["package"] == "prepay_id=wx_prepay_123"

    def test_sign_type_is_md5(self, pay_client: WeChatPayClient):
        params = pay_client.generate_payment_params("wx_prepay_123")
        assert params["signType"] == "MD5"

    def test_timestamp_is_numeric_string(self, pay_client: WeChatPayClient):
        params = pay_client.generate_payment_params("wx_prepay_123")
        assert params["timeStamp"].isdigit()


class TestCreateJsapiOrder:
    """测试 JSAPI 统一下单"""

    @pytest.mark.asyncio
    async def test_successful_order(self, pay_client: WeChatPayClient):
        mock_response_xml = (
            "<xml>"
            "<return_code>SUCCESS</return_code>"
            "<result_code>SUCCESS</result_code>"
            "<prepay_id>wx202312345678</prepay_id>"
            "</xml>"
        )

        mock_response = AsyncMock()
        mock_response.text = mock_response_xml

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            result = await pay_client.create_jsapi_order(
                order_no="TEST_ORDER_001",
                amount_cents=19900,
                description="深掼会-餐饮套餐",
                openid="oUser123456",
            )

        assert result["prepay_id"] == "wx202312345678"
        assert "payment_params" in result
        assert result["payment_params"]["package"] == "prepay_id=wx202312345678"

    @pytest.mark.asyncio
    async def test_communication_failure(self, pay_client: WeChatPayClient):
        mock_response_xml = (
            "<xml>"
            "<return_code>FAIL</return_code>"
            "<return_msg>签名错误</return_msg>"
            "</xml>"
        )

        mock_response = AsyncMock()
        mock_response.text = mock_response_xml

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            with pytest.raises(WeChatPayError) as exc_info:
                await pay_client.create_jsapi_order(
                    order_no="TEST_ORDER_002",
                    amount_cents=5000,
                    description="test",
                    openid="oUser123",
                )
            assert "通信失败" in exc_info.value.message

    @pytest.mark.asyncio
    async def test_business_failure(self, pay_client: WeChatPayClient):
        mock_response_xml = (
            "<xml>"
            "<return_code>SUCCESS</return_code>"
            "<result_code>FAIL</result_code>"
            "<err_code>ORDERPAID</err_code>"
            "<err_code_des>该订单已支付</err_code_des>"
            "</xml>"
        )

        mock_response = AsyncMock()
        mock_response.text = mock_response_xml

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            with pytest.raises(WeChatPayError) as exc_info:
                await pay_client.create_jsapi_order(
                    order_no="TEST_ORDER_003",
                    amount_cents=10000,
                    description="test",
                    openid="oUser123",
                )
            assert exc_info.value.code == "ORDERPAID"


class TestCreateRefund:
    """测试退款"""

    @pytest.mark.asyncio
    async def test_successful_refund(self, pay_client: WeChatPayClient):
        mock_response_xml = (
            "<xml>"
            "<return_code>SUCCESS</return_code>"
            "<result_code>SUCCESS</result_code>"
            "<refund_id>wx_refund_001</refund_id>"
            "<out_refund_no>REFUND_001</out_refund_no>"
            "<refund_fee>5000</refund_fee>"
            "</xml>"
        )

        mock_response = AsyncMock()
        mock_response.text = mock_response_xml

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            result = await pay_client.create_refund(
                order_no="ORDER_001",
                refund_no="REFUND_001",
                total_amount=19900,
                refund_amount=5000,
                reason="用户申请退款",
            )

        assert result["refund_id"] == "wx_refund_001"
        assert result["refund_fee"] == 5000

    @pytest.mark.asyncio
    async def test_refund_failure(self, pay_client: WeChatPayClient):
        mock_response_xml = (
            "<xml>"
            "<return_code>SUCCESS</return_code>"
            "<result_code>FAIL</result_code>"
            "<err_code>NOTENOUGH</err_code>"
            "<err_code_des>余额不足</err_code_des>"
            "</xml>"
        )

        mock_response = AsyncMock()
        mock_response.text = mock_response_xml

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            with pytest.raises(WeChatPayError) as exc_info:
                await pay_client.create_refund(
                    order_no="ORDER_002",
                    refund_no="REFUND_002",
                    total_amount=19900,
                    refund_amount=19900,
                )
            assert exc_info.value.code == "NOTENOUGH"


class TestCreateProfitSharing:
    """测试分账"""

    @pytest.mark.asyncio
    async def test_successful_sharing(self, pay_client: WeChatPayClient):
        mock_response_xml = (
            "<xml>"
            "<return_code>SUCCESS</return_code>"
            "<result_code>SUCCESS</result_code>"
            "<order_id>wx_sharing_001</order_id>"
            "<out_order_no>SHARE_001</out_order_no>"
            "</xml>"
        )

        mock_response = AsyncMock()
        mock_response.text = mock_response_xml

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            result = await pay_client.create_profit_sharing(
                transaction_id="wx_txn_001",
                receivers=[
                    {
                        "type": "MERCHANT_ID",
                        "account": "1900000001",
                        "amount": 17910,
                        "description": "商户分账",
                    }
                ],
            )

        assert result["order_id"] == "wx_sharing_001"
        assert result["transaction_id"] == "wx_txn_001"


class TestGetWeChatPayClient:
    """测试依赖注入单例"""

    def test_returns_client_instance(self):
        # 重置单例
        import app.core.wechat_pay as module
        module._wechat_pay_client = None

        with patch("app.core.wechat_pay.get_settings") as mock_settings:
            mock_settings.return_value.WECHAT_MCH_ID = "mch_test"
            mock_settings.return_value.WECHAT_PAY_KEY = "key_test"
            mock_settings.return_value.WECHAT_APP_ID = "app_test"
            mock_settings.return_value.WECHAT_PAY_NOTIFY_URL = "https://test.com/cb"

            client = get_wechat_pay_client()
            assert isinstance(client, WeChatPayClient)
            assert client.mch_id == "mch_test"

            # 第二次调用返回同一实例
            client2 = get_wechat_pay_client()
            assert client is client2

        # 清理
        module._wechat_pay_client = None
