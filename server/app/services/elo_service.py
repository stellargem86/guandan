"""ELO 积分计算服务 - K-factor 动态调整、分数更新、段位判定

核心功能：
- calculate_elo: 标准 ELO 公式计算分数变化
- get_k_factor: 根据对局数动态调整 K 值
- determine_tier: 根据分数确定段位
- record_match_result: 记录对局并更新积分/排行榜
"""

from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.redis import redis_manager
from app.models.elo import EloScore, MatchResult


def calculate_elo(
    winner_score: int,
    loser_score: int,
    k_winner: int,
    k_loser: int,
) -> tuple[int, int]:
    """计算 ELO 分数变化

    使用标准 ELO 公式：
    E = 1 / (1 + 10^((Rb - Ra) / 400))

    胜者获得分数，败者失去分数。败者分数最低为 0。

    Args:
        winner_score: 胜者当前 ELO 分
        loser_score: 败者当前 ELO 分
        k_winner: 胜者 K 因子
        k_loser: 败者 K 因子

    Returns:
        (new_winner_score, new_loser_score) 元组
    """
    # 计算期望胜率
    expected_winner = 1.0 / (1.0 + 10 ** ((loser_score - winner_score) / 400.0))
    expected_loser = 1.0 - expected_winner

    # 计算新分数
    new_winner = winner_score + round(k_winner * (1 - expected_winner))
    new_loser = loser_score + round(k_loser * (0 - expected_loser))

    # 分数不低于 0
    return new_winner, max(new_loser, 0)


def get_k_factor(total_matches: int) -> int:
    """根据总对局数确定 K 因子

    - 新手 (<30 场): K=32，分数波动大，快速定位实力
    - 成熟玩家 (>=30 场): K=16，分数趋于稳定

    Args:
        total_matches: 总对局数

    Returns:
        K 因子值 (32 或 16)
    """
    if total_matches < 30:
        return 32
    return 16


def determine_tier(score: int) -> str:
    """根据 ELO 分数确定段位

    段位划分：
    - Bronze (青铜): 0 ~ 1199
    - Silver (白银): 1200 ~ 1499
    - Gold (黄金): 1500 ~ 1799
    - Platinum (铂金): 1800 ~ 2099
    - Diamond (钻石): 2100+

    Args:
        score: ELO 分数

    Returns:
        段位字符串 (bronze/silver/gold/platinum/diamond)
    """
    if score >= 2100:
        return "diamond"
    elif score >= 1800:
        return "platinum"
    elif score >= 1500:
        return "gold"
    elif score >= 1200:
        return "silver"
    else:
        return "bronze"


async def record_match_result(
    winner_id: int,
    loser_id: int,
    db: AsyncSession,
    event_id: int | None = None,
    recorded_by: int | None = None,
) -> MatchResult:
    """记录一场对局结果并更新双方 ELO 积分

    流程：
    1. 获取双方 ELO 记录（不存在则创建默认记录）
    2. 计算新分数
    3. 更新 elo_scores 表（分数、段位、胜负场、胜率、K因子）
    4. 更新 Redis 排行榜（个人排行 + 地区排行）
    5. 创建 MatchResult 记录

    Args:
        winner_id: 胜者用户 ID
        loser_id: 败者用户 ID
        db: 数据库 Session
        event_id: 关联赛事 ID（可选）
        recorded_by: 记录者用户 ID（可选）

    Returns:
        创建的 MatchResult 对象
    """
    # 获取或创建胜者 ELO 记录
    winner_elo = await _get_or_create_elo(db, winner_id)
    loser_elo = await _get_or_create_elo(db, loser_id)

    # 保存赛前分数
    winner_score_before = winner_elo.score
    loser_score_before = loser_elo.score

    # 计算 K 因子
    k_winner = get_k_factor(winner_elo.total_matches)
    k_loser = get_k_factor(loser_elo.total_matches)

    # 计算新分数
    new_winner_score, new_loser_score = calculate_elo(
        winner_score_before, loser_score_before, k_winner, k_loser
    )

    # 更新胜者
    winner_elo.score = new_winner_score
    winner_elo.wins += 1
    winner_elo.total_matches += 1
    winner_elo.win_rate = Decimal(str(
        round(winner_elo.wins / winner_elo.total_matches, 4)
    ))
    winner_elo.k_factor = get_k_factor(winner_elo.total_matches)
    winner_elo.tier = determine_tier(new_winner_score)

    # 更新败者
    loser_elo.score = new_loser_score
    loser_elo.losses += 1
    loser_elo.total_matches += 1
    loser_elo.win_rate = Decimal(str(
        round(loser_elo.wins / loser_elo.total_matches, 4)
    ))
    loser_elo.k_factor = get_k_factor(loser_elo.total_matches)
    loser_elo.tier = determine_tier(new_loser_score)

    # 创建对局记录
    match_result = MatchResult(
        event_id=event_id,
        winner_id=winner_id,
        loser_id=loser_id,
        winner_score_before=winner_score_before,
        winner_score_after=new_winner_score,
        loser_score_before=loser_score_before,
        loser_score_after=new_loser_score,
        recorded_by=recorded_by,
    )
    db.add(match_result)
    await db.flush()

    # 更新 Redis 排行榜
    await _update_redis_rankings(winner_elo, loser_elo)

    return match_result


async def _get_or_create_elo(db: AsyncSession, user_id: int) -> EloScore:
    """获取用户的 ELO 记录，不存在则创建默认记录

    Args:
        db: 数据库 Session
        user_id: 用户 ID

    Returns:
        EloScore 对象
    """
    stmt = select(EloScore).where(EloScore.user_id == user_id)
    result = await db.execute(stmt)
    elo = result.scalar_one_or_none()

    if elo is None:
        elo = EloScore(
            user_id=user_id,
            score=1200,
            tier="silver",
            total_matches=0,
            wins=0,
            losses=0,
            win_rate=Decimal("0.0000"),
            k_factor=32,
        )
        db.add(elo)
        await db.flush()

    return elo


async def _update_redis_rankings(
    winner_elo: EloScore, loser_elo: EloScore
) -> None:
    """更新 Redis 排行榜

    更新个人排行榜，如果玩家有地区信息则同时更新地区排行榜。

    Args:
        winner_elo: 胜者 ELO 记录
        loser_elo: 败者 ELO 记录
    """
    # 更新个人排行榜
    await redis_manager.ranking_update(
        ranking_type="personal",
        member=str(winner_elo.user_id),
        score=float(winner_elo.score),
    )
    await redis_manager.ranking_update(
        ranking_type="personal",
        member=str(loser_elo.user_id),
        score=float(loser_elo.score),
    )

    # 更新地区排行榜（如果有地区信息）
    if winner_elo.region:
        await redis_manager.ranking_update(
            ranking_type="region",
            member=str(winner_elo.user_id),
            score=float(winner_elo.score),
            ranking_id=winner_elo.region,
        )
    if loser_elo.region:
        await redis_manager.ranking_update(
            ranking_type="region",
            member=str(loser_elo.user_id),
            score=float(loser_elo.score),
            ranking_id=loser_elo.region,
        )
