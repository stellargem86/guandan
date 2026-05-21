/**
 * 资讯/文章相关类型定义
 */

/** 文章分类 */
export type ArticleCategory = 'recommended' | 'news' | 'tutorial' | 'culture' | 'sports'

/** 资讯文章 */
export interface Article {
  id: number
  title: string
  /** 富文本 HTML 内容 */
  content: string
  thumbnail?: string
  category: ArticleCategory
  source: string
  author?: string
  publishTime: string
  viewCount: number
  likeCount: number
  commentCount: number
  isLiked: boolean
  isBookmarked: boolean
}

/** 文章评论 */
export interface ArticleComment {
  id: number
  articleId: number
  userId: number
  userNickname: string
  userAvatar?: string
  content: string
  createdAt: string
}
