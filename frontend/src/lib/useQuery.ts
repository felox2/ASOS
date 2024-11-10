import { type ComputedGetter, ref, watch } from 'vue'

interface UseFetchQueryOptions<T> {
  load: () => Promise<{ data?: T; error?: any }>
  immediate?: boolean
  watch?: ComputedGetter<Array<any>>
}

interface UseQueryOptions<T> {
  load: () => Promise<T>
  immediate?: boolean
  watch?: ComputedGetter<Array<string | number>>
}

export function useQuery<T>(options: UseQueryOptions<T>) {
  const data = ref<T | undefined>()
  const error = ref<any>()
  const loading = ref(false)

  function reload() {
    loading.value = true
    return options
      .load()
      .then((res) => {
        if (res) {
          data.value = res
          error.value = undefined
        }
      })
      .catch((err) => {
        data.value = undefined
        error.value = err
      })
      .finally(() => {
        loading.value = false
      })
  }

  if (options.immediate) {
    reload()
  }

  if (options.watch) {
    watch(options.watch, () => {
      reload()
    })
  }

  return {
    data,
    error,
    loading,
    reload,
  }
}

export function useFetchQuery<T>(options: UseFetchQueryOptions<T>) {
  const data = ref<T | undefined>()
  const error = ref<any>()
  const loading = ref(false)

  function reload() {
    loading.value = true
    return options
      .load()
      .then((res) => {
        if (res.data) {
          data.value = res.data
          error.value = undefined
        }
        if (res.error) {
          data.value = undefined
          error.value = res.error
        }

        return res.data
      })
      .catch((err) => {
        error.value = err
      })
      .finally(() => {
        loading.value = false
      })
  }

  if (options.immediate) {
    reload()
  }

  if (options.watch) {
    watch(
      options.watch,
      () => {
        reload()
      },
      {
        deep: true,
      },
    )
  }

  return {
    data,
    error,
    loading,
    reload,
  }
}