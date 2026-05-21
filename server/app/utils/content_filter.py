"""内容审核过滤 - 敏感词检测

提供基于关键词的简单文本过滤功能：
- SENSITIVE_WORDS: 敏感词列表（占位示例）
- filter_text(text): 检测文本是否包含敏感词

机制：先发后审 —— 创建帖子/评论时先过滤，命中敏感词则设置 status='hidden'。
"""

import re

# 敏感词列表（占位示例，实际生产环境应从数据库或配置中心加载）
SENSITIVE_WORDS: list[str] = [
    "赌博",
    "色情",
    "诈骗",
    "传销",
    "毒品",
    "枪支",
    "暴力",
    "反动",
    "邪教",
    "洗钱",
]


def filter_text(text: str) -> tuple[bool, list[str]]:
    """检测文本是否包含敏感词

    使用简单的关键词匹配（不区分大小写），检测文本中是否包含敏感词。

    Args:
        text: 待检测的文本内容

    Returns:
        (is_clean, matched_words)
        - is_clean: True 表示文本干净，无违规
        - matched_words: 命中的敏感词列表
    """
    if not text:
        return True, []

    matched_words: list[str] = []
    text_lower = text.lower()

    for word in SENSITIVE_WORDS:
        if word.lower() in text_lower:
            matched_words.append(word)

    is_clean = len(matched_words) == 0
    return is_clean, matched_words
