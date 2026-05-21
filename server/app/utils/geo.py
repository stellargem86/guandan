"""地理位置工具函数 - Haversine 距离计算 + GeoHash 编码

提供纯计算工具：
- haversine_distance: 两点间球面距离 (km)
- encode_geohash: 经纬度转 GeoHash 字符串
"""

import math

# 地球平均半径 (km)
EARTH_RADIUS_KM = 6371.0

# GeoHash 使用的 Base32 字符集
_GEOHASH_BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"


def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """使用 Haversine 公式计算两点间的球面距离

    Args:
        lat1: 第一个点的纬度 (度)
        lng1: 第一个点的经度 (度)
        lat2: 第二个点的纬度 (度)
        lng2: 第二个点的经度 (度)

    Returns:
        两点间的距离，单位为公里 (km)
    """
    # 将度转换为弧度
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)

    # Haversine 公式
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlng / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return EARTH_RADIUS_KM * c


def encode_geohash(lat: float, lng: float, precision: int = 8) -> str:
    """将经纬度编码为 GeoHash 字符串

    Args:
        lat: 纬度 (-90 ~ 90)
        lng: 经度 (-180 ~ 180)
        precision: 精度位数，默认 8 (约 19m x 19m)

    Returns:
        GeoHash 编码字符串
    """
    lat_range = (-90.0, 90.0)
    lng_range = (-180.0, 180.0)

    geohash_chars: list[str] = []
    bits = 0
    char_index = 0
    is_lng_bit = True  # 经度和纬度交替编码，经度先行

    while len(geohash_chars) < precision:
        if is_lng_bit:
            mid = (lng_range[0] + lng_range[1]) / 2
            if lng >= mid:
                char_index = (char_index << 1) | 1
                lng_range = (mid, lng_range[1])
            else:
                char_index = char_index << 1
                lng_range = (lng_range[0], mid)
        else:
            mid = (lat_range[0] + lat_range[1]) / 2
            if lat >= mid:
                char_index = (char_index << 1) | 1
                lat_range = (mid, lat_range[1])
            else:
                char_index = char_index << 1
                lat_range = (lat_range[0], mid)

        is_lng_bit = not is_lng_bit
        bits += 1

        if bits == 5:
            geohash_chars.append(_GEOHASH_BASE32[char_index])
            bits = 0
            char_index = 0

    return "".join(geohash_chars)
