import { Property } from '@/lib/composables/useLayoutProperties'
import {
  PaginationState,
  SortingState,
  VisibilityState,
} from '@tanstack/vue-table'
import { refDebounced } from '@vueuse/core'
import { MaybeRefOrGetter, ref, toValue, watch } from 'vue'

interface Props {
  visibility: VisibilityState
}

export function useTableState(
  propertiesRef: MaybeRefOrGetter<Property[]>,
  defaults?: Props,
) {
  const fulltextFilter = ref('')
  const fulltextFilterDebounced = refDebounced(fulltextFilter, 200)
  const sorting = ref<SortingState>([])
  const visibility = ref<VisibilityState>({})
  const pagination = ref<PaginationState>({
    pageIndex: 0,
    pageSize: 10,
  })

  if (propertiesRef) {
    watch(
      propertiesRef,
      () => {
        const properties = toValue(propertiesRef)
        if (!properties) {
          return
        }

        let temp: Record<string, boolean> = {}

        for (const property of properties) {
          temp[property.dbPath] = false
        }

        visibility.value = {
          ...temp,
          ...(defaults?.visibility ?? {}),
        }
      },
      {
        immediate: true,
      },
    )
  }

  return {
    fulltextFilter,
    fulltextFilterDebounced,
    sorting,
    pagination,
    visibility,
  }
}
