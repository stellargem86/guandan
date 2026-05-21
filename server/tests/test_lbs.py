"""LBS 地理位置服务测试 - Haversine 距离 + GeoHash 编码

验证 geo.py 工具函数的正确性：
- haversine_distance: 已知距离验证
- encode_geohash: 编码正确性
"""

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from app.utils.geo import encode_geohash, haversine_distance


class TestHaversineDistance:
    """Haversine 距离计算测试"""

    def test_same_point_zero_distance(self):
        """同一点距离为 0"""
        assert haversine_distance(31.23, 121.47, 31.23, 121.47) == 0.0

    def test_known_distance_shanghai_to_beijing(self):
        """上海到北京约 1068 km"""
        # 上海: 31.2304, 121.4737
        # 北京: 39.9042, 116.4074
        dist = haversine_distance(31.2304, 121.4737, 39.9042, 116.4074)
        # 已知距离约 1068 km，允许 ±50 km 误差
        assert 1000 < dist < 1120

    def test_known_distance_short(self):
        """短距离验证 (~1.1 km)"""
        # 两个很近的点
        dist = haversine_distance(31.230, 121.470, 31.240, 121.470)
        # 纬度差 0.01 度约 1.11 km
        assert 1.0 < dist < 1.2

    def test_symmetry(self):
        """距离对称性: d(A,B) = d(B,A)"""
        d1 = haversine_distance(31.0, 121.0, 39.0, 116.0)
        d2 = haversine_distance(39.0, 116.0, 31.0, 121.0)
        assert abs(d1 - d2) < 1e-10

    @given(
        lat=st.floats(min_value=-90, max_value=90),
        lng=st.floats(min_value=-180, max_value=180),
    )
    @settings(max_examples=100)
    def test_self_distance_always_zero(self, lat: float, lng: float):
        """属性: 任何点到自身的距离为 0"""
        assert haversine_distance(lat, lng, lat, lng) == 0.0

    @given(
        lat1=st.floats(min_value=-90, max_value=90),
        lng1=st.floats(min_value=-180, max_value=180),
        lat2=st.floats(min_value=-90, max_value=90),
        lng2=st.floats(min_value=-180, max_value=180),
    )
    @settings(max_examples=100)
    def test_distance_always_non_negative(
        self, lat1: float, lng1: float, lat2: float, lng2: float
    ):
        """属性: 距离永远非负"""
        dist = haversine_distance(lat1, lng1, lat2, lng2)
        assert dist >= 0.0

    @given(
        lat1=st.floats(min_value=-90, max_value=90),
        lng1=st.floats(min_value=-180, max_value=180),
        lat2=st.floats(min_value=-90, max_value=90),
        lng2=st.floats(min_value=-180, max_value=180),
    )
    @settings(max_examples=100)
    def test_distance_max_half_earth(
        self, lat1: float, lng1: float, lat2: float, lng2: float
    ):
        """属性: 距离不超过地球半周长 (~20015 km)"""
        dist = haversine_distance(lat1, lng1, lat2, lng2)
        assert dist <= 20020  # 半周长约 20015 km


class TestEncodeGeohash:
    """GeoHash 编码测试"""

    def test_precision_length(self):
        """输出长度等于精度"""
        gh = encode_geohash(31.23, 121.47, precision=8)
        assert len(gh) == 8

    def test_known_geohash(self):
        """已知编码验证 - 上海浦东区域前缀"""
        gh = encode_geohash(31.23, 121.47, precision=6)
        # 上海浦东区域的 GeoHash 前缀应以 'wt' 开头
        assert gh.startswith("wt")

    def test_different_precision(self):
        """不同精度的前缀一致"""
        gh6 = encode_geohash(31.23, 121.47, precision=6)
        gh8 = encode_geohash(31.23, 121.47, precision=8)
        # 高精度的前缀应包含低精度
        assert gh8.startswith(gh6)

    def test_nearby_points_share_prefix(self):
        """相近点共享 GeoHash 前缀"""
        gh1 = encode_geohash(31.230, 121.470, precision=6)
        gh2 = encode_geohash(31.231, 121.471, precision=6)
        # 非常近的点应该共享前几位
        assert gh1[:4] == gh2[:4]

    @given(
        lat=st.floats(min_value=-90, max_value=90),
        lng=st.floats(min_value=-180, max_value=180),
        precision=st.integers(min_value=1, max_value=12),
    )
    @settings(max_examples=100)
    def test_output_length_matches_precision(
        self, lat: float, lng: float, precision: int
    ):
        """属性: 输出长度总是等于指定精度"""
        gh = encode_geohash(lat, lng, precision=precision)
        assert len(gh) == precision

    @given(
        lat=st.floats(min_value=-90, max_value=90),
        lng=st.floats(min_value=-180, max_value=180),
    )
    @settings(max_examples=100)
    def test_only_valid_base32_chars(self, lat: float, lng: float):
        """属性: 输出只包含合法的 GeoHash Base32 字符"""
        valid_chars = set("0123456789bcdefghjkmnpqrstuvwxyz")
        gh = encode_geohash(lat, lng, precision=8)
        assert all(c in valid_chars for c in gh)
