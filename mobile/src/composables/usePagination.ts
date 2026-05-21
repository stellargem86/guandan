/**
 * 分页与无限滚动组合函数
 */
import { ref } from 'vue'

interface PaginationOptions<T> {
  fetchFn: (params: { page: number; pageSize: number }) => Promise<{ data: T[] }>
  pageSize?: number
}

export function usePagination<T>(options: PaginationOptions<T>) {
  const { fetchFn, pageSize = 20 } = options

  const list = ref<T[]>([]) as { value: T[] }
  const page = ref(1)
  const loading = ref(false)
  const finished = ref(false)
  const refreshing = ref(false)

  /** 加载更多 */
  async function loadMore() {
    if (loading.value || finished.value) return

    loading.value = true
    try {
      const res = await fetchFn({ page: page.value, pageSize })
      if (res.data.length < pageSize) {
        finished.value = true
      }
      list.value.push(...res.data)
      page.value++
    } finally {
      loading.value = false
    }
  }

  /** 下拉刷新 */
  async function refresh() {
    refreshing.value = true
    page.value = 1
    finished.value = false
    list.value = []
    await loadMore()
    refreshing.value = false
  }

  return {
    list,
    loading,
    finished,
    refreshing,
    loadMore,
    refresh,
  }
}
