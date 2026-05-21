"""内容服务测试 - 敏感词过滤、帖子 CRUD 逻辑"""

import pytest

from app.utils.content_filter import filter_text, SENSITIVE_WORDS
from app.services.content_service import check_content


class TestContentFilter:
    """敏感词过滤测试"""

    def test_clean_text_passes(self):
        """正常文本应通过审核"""
        is_clean, matched = filter_text("今天打了一局掼蛋，很开心！")
        assert is_clean is True
        assert matched == []

    def test_sensitive_word_detected(self):
        """包含敏感词应被检测到"""
        is_clean, matched = filter_text("这里有赌博信息")
        assert is_clean is False
        assert "赌博" in matched

    def test_multiple_sensitive_words(self):
        """多个敏感词同时命中"""
        is_clean, matched = filter_text("赌博和色情都是违法的")
        assert is_clean is False
        assert "赌博" in matched
        assert "色情" in matched

    def test_empty_text_passes(self):
        """空文本应通过审核"""
        is_clean, matched = filter_text("")
        assert is_clean is True
        assert matched == []

    def test_check_content_wrapper(self):
        """check_content 应正确代理 filter_text"""
        is_clean, violations = check_content("正常内容")
        assert is_clean is True
        assert violations == []

        is_clean, violations = check_content("包含毒品信息")
        assert is_clean is False
        assert "毒品" in violations
