"""文章服务 & 广告服务单元测试 - Tasks 11.1, 11.2

测试内容：
- 文章 CRUD 操作（创建、列表、详情、更新、删除）
- 文章分类验证
- 广告获取、曝光/点击追踪
- 广告创建和更新
"""

from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.article_service import (
    ArticleServiceError,
    VALID_CATEGORIES as ARTICLE_CATEGORIES,
    create_article,
    get_articles,
    get_article_detail,
    update_article,
    delete_article,
)
from app.services.ad_service import (
    AdServiceError,
    VALID_POSITIONS,
    create_ad,
    get_active_ads,
    record_impression,
    record_click,
    update_ad,
)


# ─── Task 11.1: 文章服务测试 ──────────────────────────────────────────


class TestArticleServiceValidation:
    """文章服务参数验证测试"""

    def test_valid_categories(self):
        """文章分类包含指定的4种"""
        assert "news" in ARTICLE_CATEGORIES
        assert "tutorial" in ARTICLE_CATEGORIES
        assert "culture" in ARTICLE_CATEGORIES
        assert "strategy" in ARTICLE_CATEGORIES
        assert len(ARTICLE_CATEGORIES) == 4

    @pytest.mark.asyncio
    async def test_create_article_invalid_category_raises(self):
        """创建文章时无效分类抛出异常"""
        db = AsyncMock()

        with pytest.raises(ArticleServiceError) as exc_info:
            await create_article(
                db=db,
                title="测试文章",
                content="内容",
                category="invalid_category",
                author_id=1,
            )

        assert exc_info.value.code == "INVALID_CATEGORY"

    @pytest.mark.asyncio
    @patch("app.services.article_service.Article")
    async def test_create_article_valid_category(self, MockArticle):
        """创建文章时有效分类正常创建"""
        db = AsyncMock()
        db.add = MagicMock()
        db.flush = AsyncMock()

        mock_article = MagicMock()
        MockArticle.return_value = mock_article

        article = await create_article(
            db=db,
            title="测试文章",
            content="这是文章内容",
            category="news",
            author_id=1,
            cover_image="https://example.com/img.jpg",
        )

        MockArticle.assert_called_once_with(
            title="测试文章",
            content="这是文章内容",
            category="news",
            author_id=1,
            cover_image="https://example.com/img.jpg",
            status="published",
        )
        assert article == mock_article
        db.add.assert_called_once_with(mock_article)
        db.flush.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_get_articles_invalid_category_raises(self):
        """获取文章列表时无效分类抛出异常"""
        db = AsyncMock()

        with pytest.raises(ArticleServiceError) as exc_info:
            await get_articles(db=db, category="bogus")

        assert exc_info.value.code == "INVALID_CATEGORY"

    @pytest.mark.asyncio
    async def test_get_article_detail_not_found_raises(self):
        """获取不存在的文章详情抛出异常"""
        db = AsyncMock()

        # Mock execute for update (returns rowcount)
        mock_update_result = MagicMock()
        mock_update_result.rowcount = 0

        # Mock execute for select (returns None)
        mock_select_result = MagicMock()
        mock_select_result.scalar_one_or_none.return_value = None

        db.execute = AsyncMock(side_effect=[mock_update_result, mock_select_result])

        with pytest.raises(ArticleServiceError) as exc_info:
            await get_article_detail(db=db, article_id=999)

        assert exc_info.value.code == "ARTICLE_NOT_FOUND"

    @pytest.mark.asyncio
    async def test_update_article_invalid_category_raises(self):
        """更新文章时无效分类抛出异常"""
        db = AsyncMock()

        with pytest.raises(ArticleServiceError) as exc_info:
            await update_article(db=db, article_id=1, category="invalid")

        assert exc_info.value.code == "INVALID_CATEGORY"

    @pytest.mark.asyncio
    async def test_update_article_no_updates_raises(self):
        """更新文章时没有有效字段抛出异常"""
        db = AsyncMock()

        with pytest.raises(ArticleServiceError) as exc_info:
            await update_article(db=db, article_id=1)

        assert exc_info.value.code == "NO_UPDATES"

    @pytest.mark.asyncio
    async def test_update_article_not_found_raises(self):
        """更新不存在的文章抛出异常"""
        db = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = 0
        db.execute = AsyncMock(return_value=mock_result)

        with pytest.raises(ArticleServiceError) as exc_info:
            await update_article(db=db, article_id=999, title="新标题")

        assert exc_info.value.code == "ARTICLE_NOT_FOUND"

    @pytest.mark.asyncio
    async def test_delete_article_not_found_raises(self):
        """删除不存在的文章抛出异常"""
        db = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = 0
        db.execute = AsyncMock(return_value=mock_result)

        with pytest.raises(ArticleServiceError) as exc_info:
            await delete_article(db=db, article_id=999)

        assert exc_info.value.code == "ARTICLE_NOT_FOUND"

    @pytest.mark.asyncio
    async def test_delete_article_success(self):
        """成功删除文章（软删除）"""
        db = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = 1
        db.execute = AsyncMock(return_value=mock_result)

        result = await delete_article(db=db, article_id=1)
        assert result is True


# ─── Task 11.2: 广告服务测试 ──────────────────────────────────────────


class TestAdServiceValidation:
    """广告服务参数验证测试"""

    def test_valid_positions(self):
        """广告位置包含指定的4种"""
        assert "home_banner" in VALID_POSITIONS
        assert "feed_card" in VALID_POSITIONS
        assert "event_banner" in VALID_POSITIONS
        assert "news_feed" in VALID_POSITIONS
        assert len(VALID_POSITIONS) == 4

    @pytest.mark.asyncio
    async def test_get_active_ads_invalid_position_raises(self):
        """获取广告时无效位置抛出异常"""
        db = AsyncMock()

        with pytest.raises(AdServiceError) as exc_info:
            await get_active_ads(db=db, position="invalid_position")

        assert exc_info.value.code == "INVALID_POSITION"

    @pytest.mark.asyncio
    async def test_create_ad_invalid_position_raises(self):
        """创建广告时无效位置抛出异常"""
        db = AsyncMock()

        with pytest.raises(AdServiceError) as exc_info:
            await create_ad(
                db=db,
                title="广告",
                image_url="https://example.com/ad.jpg",
                link_url="https://example.com",
                position="invalid_pos",
            )

        assert exc_info.value.code == "INVALID_POSITION"

    @pytest.mark.asyncio
    @patch("app.services.ad_service.Advertisement")
    async def test_create_ad_valid(self, MockAdvertisement):
        """创建广告成功"""
        db = AsyncMock()
        db.add = MagicMock()
        db.flush = AsyncMock()

        mock_ad = MagicMock()
        MockAdvertisement.return_value = mock_ad

        ad = await create_ad(
            db=db,
            title="首页横幅广告",
            image_url="https://example.com/banner.jpg",
            link_url="https://example.com/promo",
            position="home_banner",
            start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2024, 12, 31, tzinfo=timezone.utc),
        )

        MockAdvertisement.assert_called_once_with(
            title="首页横幅广告",
            image_url="https://example.com/banner.jpg",
            link_url="https://example.com/promo",
            position="home_banner",
            start_date=datetime(2024, 1, 1, tzinfo=timezone.utc),
            end_date=datetime(2024, 12, 31, tzinfo=timezone.utc),
            status="active",
        )
        assert ad == mock_ad
        db.add.assert_called_once_with(mock_ad)
        db.flush.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_record_impression_not_found_raises(self):
        """记录曝光时广告不存在抛出异常"""
        db = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = 0
        db.execute = AsyncMock(return_value=mock_result)

        with pytest.raises(AdServiceError) as exc_info:
            await record_impression(db=db, ad_id=999)

        assert exc_info.value.code == "AD_NOT_FOUND"

    @pytest.mark.asyncio
    async def test_record_impression_success(self):
        """记录曝光成功"""
        db = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = 1
        db.execute = AsyncMock(return_value=mock_result)

        # Should not raise
        await record_impression(db=db, ad_id=1)
        db.execute.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_record_click_not_found_raises(self):
        """记录点击时广告不存在抛出异常"""
        db = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = 0
        db.execute = AsyncMock(return_value=mock_result)

        with pytest.raises(AdServiceError) as exc_info:
            await record_click(db=db, ad_id=999)

        assert exc_info.value.code == "AD_NOT_FOUND"

    @pytest.mark.asyncio
    async def test_record_click_success(self):
        """记录点击成功"""
        db = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = 1
        db.execute = AsyncMock(return_value=mock_result)

        await record_click(db=db, ad_id=1)
        db.execute.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_update_ad_invalid_position_raises(self):
        """更新广告时无效位置抛出异常"""
        db = AsyncMock()

        with pytest.raises(AdServiceError) as exc_info:
            await update_ad(db=db, ad_id=1, position="bad_pos")

        assert exc_info.value.code == "INVALID_POSITION"

    @pytest.mark.asyncio
    async def test_update_ad_no_updates_raises(self):
        """更新广告时没有有效字段抛出异常"""
        db = AsyncMock()

        with pytest.raises(AdServiceError) as exc_info:
            await update_ad(db=db, ad_id=1)

        assert exc_info.value.code == "NO_UPDATES"

    @pytest.mark.asyncio
    async def test_update_ad_not_found_raises(self):
        """更新不存在的广告抛出异常"""
        db = AsyncMock()
        mock_result = MagicMock()
        mock_result.rowcount = 0
        db.execute = AsyncMock(return_value=mock_result)

        with pytest.raises(AdServiceError) as exc_info:
            await update_ad(db=db, ad_id=999, title="新标题")

        assert exc_info.value.code == "AD_NOT_FOUND"
