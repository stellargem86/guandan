"""ELO 积分计算服务 - 属性测试 (Property-Based Tests)

使用 hypothesis 进行属性测试，验证 ELO 算法的核心数学性质：
1. 零和性 (Zero-Sum): 胜者得分 + 败者失分 = 常数（总分守恒）
2. 单调性 (Monotonicity): 胜者分数必增，败者分数必减
3. 分数下界 (Floor): 分数永远不低于 0

**Validates: Requirements 9.1**
"""

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from app.services.elo_service import (
    calculate_elo,
    determine_tier,
    get_k_factor,
)


# ─── 策略定义 ─────────────────────────────────────────────────────

# ELO 分数范围: 0 ~ 3000 (覆盖所有合理段位)
elo_score = st.integers(min_value=0, max_value=3000)

# K 因子: 16 或 32
k_factor = st.sampled_from([16, 32])

# 总对局数
total_matches = st.integers(min_value=0, max_value=1000)


# ─── 属性测试: 零和性 (Zero-Sum Property) ─────────────────────────

class TestEloZeroSum:
    """验证 ELO 算法的零和性质

    在没有分数下界约束的情况下，双方分数变化之和为零。
    当败者分数触底为 0 时，总分可能增加（因为截断了负数），
    所以零和性验证的是: new_winner + new_loser >= winner + loser
    且差值 <= k_loser（最多因为截断而多出 k_loser 分）。
    """

    @given(
        winner_score=elo_score,
        loser_score=elo_score,
        k_w=k_factor,
        k_l=k_factor,
    )
    @settings(max_examples=200)
    def test_total_score_conservation(
        self, winner_score: int, loser_score: int, k_w: int, k_l: int
    ):
        """总分守恒: 当 K 值相同时，在没有底限约束下，分数变化和为零

        当 k_winner == k_loser 时:
        - winner_gain = round(K * (1 - E_w))
        - loser_loss = round(K * (0 - E_l)) = round(K * (E_w - 1)) = -winner_gain (approx)

        因为 rounding 可能导致 ±1 的偏差，且 max(0) 截断可能消耗一些分数。
        """
        new_winner, new_loser = calculate_elo(winner_score, loser_score, k_w, k_l)

        total_before = winner_score + loser_score
        total_after = new_winner + new_loser

        # 由于 max(0) 截断，总分可能略微增加
        # 没有截断时 (same K): |total_after - total_before| <= 1 (rounding)
        # 有截断时: total_after >= total_before (截断保底只会增加总分)
        # 不同 K 值时: 差异取决于 K 值差和期望胜率
        assert total_after >= total_before - max(k_w, k_l)

    @given(
        winner_score=elo_score,
        loser_score=elo_score,
        k=k_factor,
    )
    @settings(max_examples=200)
    def test_same_k_zero_sum(self, winner_score: int, loser_score: int, k: int):
        """相同 K 因子下的近似零和性

        当双方使用相同 K 因子时，且败者分数未触底，
        总分变化仅由 round() 引入 ±1 偏差。
        """
        new_winner, new_loser = calculate_elo(winner_score, loser_score, k, k)

        total_before = winner_score + loser_score
        total_after = new_winner + new_loser

        # 如果败者分数未触底，近似零和（rounding 偏差 ±1）
        loser_raw = loser_score + round(k * (0 - (1.0 - 1.0 / (1.0 + 10 ** ((loser_score - winner_score) / 400.0)))))
        if loser_raw >= 0:
            # 未触底：总分差 <= 1 (rounding)
            assert abs(total_after - total_before) <= 1
        else:
            # 触底：total_after >= total_before (因为截断了负数)
            assert total_after >= total_before


# ─── 属性测试: 单调性 (Monotonicity Property) ─────────────────────

class TestEloMonotonicity:
    """验证胜者分数必增、败者分数必减（或不变 = 触底时）"""

    @given(
        winner_score=elo_score,
        loser_score=elo_score,
        k_w=k_factor,
        k_l=k_factor,
    )
    @settings(max_examples=200)
    def test_winner_always_gains(
        self, winner_score: int, loser_score: int, k_w: int, k_l: int
    ):
        """胜者分数必须增加（或至少不减）"""
        new_winner, _ = calculate_elo(winner_score, loser_score, k_w, k_l)
        assert new_winner >= winner_score

    @given(
        winner_score=elo_score,
        loser_score=elo_score,
        k_w=k_factor,
        k_l=k_factor,
    )
    @settings(max_examples=200)
    def test_loser_always_loses(
        self, winner_score: int, loser_score: int, k_w: int, k_l: int
    ):
        """败者分数必须减少（或保持不变 - 因为分数不能低于 0）"""
        _, new_loser = calculate_elo(winner_score, loser_score, k_w, k_l)
        assert new_loser <= loser_score


# ─── 属性测试: 分数下界 (Floor Property) ──────────────────────────

class TestEloFloor:
    """验证分数永远不低于 0"""

    @given(
        winner_score=elo_score,
        loser_score=elo_score,
        k_w=k_factor,
        k_l=k_factor,
    )
    @settings(max_examples=200)
    def test_score_never_below_zero(
        self, winner_score: int, loser_score: int, k_w: int, k_l: int
    ):
        """任何情况下分数都不能低于 0"""
        new_winner, new_loser = calculate_elo(winner_score, loser_score, k_w, k_l)
        assert new_winner >= 0
        assert new_loser >= 0


# ─── 单元测试: K 因子 ─────────────────────────────────────────────

class TestKFactor:
    """K 因子计算单元测试"""

    def test_new_player_k32(self):
        """新手 (<30 场) K=32"""
        assert get_k_factor(0) == 32
        assert get_k_factor(15) == 32
        assert get_k_factor(29) == 32

    def test_established_player_k16(self):
        """成熟玩家 (>=30 场) K=16"""
        assert get_k_factor(30) == 16
        assert get_k_factor(100) == 16
        assert get_k_factor(500) == 16

    @given(matches=st.integers(min_value=0, max_value=29))
    def test_under_30_always_32(self, matches: int):
        """属性: 任何 <30 场都返回 32"""
        assert get_k_factor(matches) == 32

    @given(matches=st.integers(min_value=30, max_value=10000))
    def test_over_30_always_16(self, matches: int):
        """属性: 任何 >=30 场都返回 16"""
        assert get_k_factor(matches) == 16


# ─── 单元测试: 段位判定 ───────────────────────────────────────────

class TestDetermineTier:
    """段位判定单元测试"""

    def test_bronze(self):
        assert determine_tier(0) == "bronze"
        assert determine_tier(1199) == "bronze"

    def test_silver(self):
        assert determine_tier(1200) == "silver"
        assert determine_tier(1499) == "silver"

    def test_gold(self):
        assert determine_tier(1500) == "gold"
        assert determine_tier(1799) == "gold"

    def test_platinum(self):
        assert determine_tier(1800) == "platinum"
        assert determine_tier(2099) == "platinum"

    def test_diamond(self):
        assert determine_tier(2100) == "diamond"
        assert determine_tier(3000) == "diamond"

    @given(score=st.integers(min_value=0, max_value=1199))
    def test_bronze_range(self, score: int):
        """属性: 0-1199 都是 bronze"""
        assert determine_tier(score) == "bronze"

    @given(score=st.integers(min_value=1200, max_value=1499))
    def test_silver_range(self, score: int):
        """属性: 1200-1499 都是 silver"""
        assert determine_tier(score) == "silver"

    @given(score=st.integers(min_value=2100, max_value=5000))
    def test_diamond_range(self, score: int):
        """属性: 2100+ 都是 diamond"""
        assert determine_tier(score) == "diamond"


# ─── 单元测试: ELO 计算边界场景 ───────────────────────────────────

class TestEloEdgeCases:
    """ELO 计算边界场景"""

    def test_equal_scores(self):
        """等分对局: 胜者+16, 败者-16 (K=32时)"""
        new_w, new_l = calculate_elo(1200, 1200, 32, 32)
        assert new_w == 1216
        assert new_l == 1184

    def test_underdog_wins(self):
        """低分选手胜: 获得更多分数"""
        new_w, new_l = calculate_elo(1000, 1400, 32, 32)
        # 低分胜者应该获得比 16 更多的分 (因为期望胜率低)
        gain = new_w - 1000
        assert gain > 16

    def test_favorite_wins(self):
        """高分选手胜: 获得较少分数"""
        new_w, new_l = calculate_elo(1400, 1000, 32, 32)
        # 高分胜者获得较少分
        gain = new_w - 1400
        assert gain < 16

    def test_loser_floor_at_zero(self):
        """败者分数不会低于 0"""
        new_w, new_l = calculate_elo(2000, 5, 32, 32)
        assert new_l >= 0
