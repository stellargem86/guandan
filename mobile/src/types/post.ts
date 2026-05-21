/**
 * 帖子/掼友圈内容类型定义
 */

export interface Post {
  id: number
  user_id: number
  user_nickname: string
  user_avatar?: string
  content: string
  images: string[]
  like_count: number
  comment_count: number
  is_liked: boolean
  created_at: string
}

export interface Comment {
  id: number
  post_id: number
  user_id: number
  user_nickname: string
  user_avatar?: string
  content: string
  reply_to?: number
  created_at: string
}

export interface CreatePostParams {
  content: string
  images?: string[]
}
