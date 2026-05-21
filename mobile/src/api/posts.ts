/**
 * 掼友圈帖子相关 API
 */
import { request } from './index'

/** 获取帖子列表 */
export function getPosts(params: { page: number; pageSize: number }) {
  return request({
    url: '/api/v1/posts',
    method: 'GET',
    data: params,
  })
}

/** 发布帖子 */
export function createPost(data: { content: string; images?: string[] }) {
  return request({
    url: '/api/v1/posts',
    method: 'POST',
    data,
  })
}

/** 点赞 */
export function likePost(postId: number) {
  return request({
    url: `/api/v1/posts/${postId}/like`,
    method: 'POST',
  })
}

/** 取消点赞 */
export function unlikePost(postId: number) {
  return request({
    url: `/api/v1/posts/${postId}/like`,
    method: 'DELETE',
  })
}
