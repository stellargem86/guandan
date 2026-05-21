/**
 * 数字钱包相关 API
 */
import { request } from './index'

/** 获取钱包信息 */
export function getWalletInfo() {
  return request({
    url: '/api/v1/wallet',
    method: 'GET',
  })
}

/** 获取交易流水 */
export function getTransactions(params?: { page?: number; pageSize?: number }) {
  return request({
    url: '/api/v1/wallet/transactions',
    method: 'GET',
    data: params,
  })
}

/** 发起提现 */
export function withdraw(data: { amount: number }) {
  return request({
    url: '/api/v1/wallet/withdraw',
    method: 'POST',
    data,
  })
}
