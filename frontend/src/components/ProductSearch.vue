<script setup lang="ts">
import { useFetchQuery } from '@/composables/useQuery'
import { client } from '@/lib/client'
import { cn } from '@/lib/utils'
import { onClickOutside, useDebounce } from '@vueuse/core'
import { Search } from 'lucide-vue-next'
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { Input } from './ui/input'

const { t, n } = useI18n()

const open = ref(false)
const query = ref('')
const container = ref()
const queryDebounced = useDebounce(query, 300)

const { data: items } = useFetchQuery({
  watch: () => [queryDebounced.value],
  load: () =>
    queryDebounced.value.length > 2
      ? client.GET('/api/products', {
          params: {
            query: {
              search: queryDebounced.value,
            },
          },
        })
      : Promise.resolve({ data: [] }),
})

function close() {
  open.value = false
  query.value = ''
}

onClickOutside(container, () => {
  open.value = false
})
</script>

<template>
  <div class="relative" ref="container">
    <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />

    <Input
      class="pl-8 w-full sm:w-[300px] md:w-[400px] lg:w-[500px]"
      type="text"
      v-model="query"
      :placeholder="t('search')"
      @focus="open = true"
    />

    <div
      v-if="items"
      :class="
        cn(
          'absolute z-50 top-[calc(100%_+_4px)] w-full rounded-md border bg-popover text-popover-foreground shadow-md outline-none pointer-events-none opacity-0 transition-opacity',
          open && 'pointer-events-auto opacity-100'
        )
      "
    >
      <div class="max-h-[300px] p-1 overflow-y-auto overflow-x-hidden">
        <p v-if="!items.length" class="px-2 py-2 pl-8 text-muted-foreground">
          {{ t('empty') }}
        </p>

        <RouterLink
          v-for="item in items"
          @click="close"
          :key="item.id"
          :to="{ name: '//products/[id]', params: { id: item.id } }"
          class="flex gap-2 rounded-sm p-2 hover:bg-accent"
        >
          <img
            v-if="item.photo"
            class="size-12 rounded aspect-square"
            :src="item.photo"
          />

          <div class="w-full">
            <div class="flex justify-between w-full">
              <h4>{{ item.name }}</h4>
            </div>
            <div class="flex justify-between items-center w-full">
              <span class="text-sm text-muted-foreground">
                {{ item.description }}
              </span>
              <span>{{ n(item.price || 0, 'currency') }}</span>
            </div>
          </div>
        </RouterLink>

        <!-- <div
          v-for="item in items"
          :key="item.id"
          class="flex flex-col relative w-full cursor-default select-none rounded-sm px-2 pl-8 py-2 outline-none hover:bg-accent"
        >
          <span>
            {{ item.name }}
          </span>
        </div> -->
      </div>
    </div>
  </div>
</template>
