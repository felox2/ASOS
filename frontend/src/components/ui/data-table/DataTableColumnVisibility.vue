<script setup lang="ts">
import { Button } from '@/components/ui/button'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { Column, Table } from '@tanstack/vue-table'
import { Check, ChevronDown, Search } from 'lucide-vue-next'
import {
  ListboxContent,
  ListboxFilter,
  ListboxItem,
  ListboxItemIndicator,
  ListboxRoot,
  ListboxVirtualizer,
} from 'radix-vue'
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'

interface Item {
  id: string
  value: string
  parent?: string
}

const { t } = useI18n()
const props = defineProps<{ table: Table<any> }>()
const open = ref(false)
const filter = ref('')
const items = computed(() =>
  props.table
    .getAllColumns()
    .filter((column) => column.getCanHide())
    .map((column) => {
      const meta = column.columnDef?.meta as any

      return {
        id: column.id as string,
        parent: meta?.parentId ? t(meta?.parentId) : undefined,
        value: t(meta?.attributeId ?? column.id),
      }
    }),
)

const selectedItems = computed(() =>
  props.table
    .getAllColumns()
    .filter((c) => c.getCanHide() && c.getIsVisible())
    .map((c) => c.id),
)

function normalize(str: string) {
  return str
    .toLowerCase()
    .normalize('NFD')
    .replace(/\p{Diacritic}/gu, '')
}

const valuesNormalized = computed(() =>
  items.value.map((i) => normalize(i.value)),
)

const itemsFiltered = computed(() => {
  const query = filter.value ? normalize(filter.value) : filter.value

  if (!query) {
    return items.value
  }

  const filtered: Item[] = []

  for (let i = 0; i < items.value.length; i++) {
    const v = valuesNormalized.value[i]

    if (v.includes(query)) {
      filtered.push(items.value[i])
    }
  }

  return filtered
})

function handleSelect(value: any) {
  const added: string[] = []
  const removed: string[] = []
  const oldItems = new Set(selectedItems.value)
  const newItems = new Set(value)

  for (const item of value) {
    if (!oldItems.has(item)) {
      added.push(item)
    }
  }

  for (const item of selectedItems.value) {
    if (!newItems.has(item)) {
      removed.push(item)
    }
  }

  for (const item of added) {
    props.table.getColumn(item)?.toggleVisibility(true)
  }
  for (const item of removed) {
    props.table.getColumn(item)?.toggleVisibility(false)
  }
}
</script>

<template>
  <Popover v-model:open="open">
    <ListboxRoot
      multiple
      :model-value="selectedItems"
      @update:modelValue="handleSelect"
    >
      <PopoverTrigger as-child>
        <slot name="trigger">
          <Button
            v-bind="$attrs"
            variant="outline"
            role="combobox"
            :aria-expanded="open"
            class="flex text-base h-12 font-normal min-w-40 w-full items-center justify-between shadow-sm border border-input rounded-md bg-background px-3 py-2 focus:outline-none disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1 text-black relative group aria-invalid:border-red aria-invalid:bg-light-red aria-invalid:text-red aria-invalid:focus-visible:bg-background aria-invalid:focus-visible:text-black aria-invalid:focus-visible:placeholder:text-black/25 aria-invalid:focus-visible:shadow-light-red"
          >
            <!-- <span
              :data-open="open || hasValue ? 'true' : undefined"
              :data-value="hasValue ? 'true' : undefined"
              class="text-muted-foreground origin-top-left transition-transform data-[value]:absolute data-[open]:scale-75 data-[open]:-translate-y-3 group-aria-invalid:text-red"
            >
              {{ placeholder ?? '' }}
            </span>
            <span v-if="valueLabel" class="mt-2">
              {{ valueLabel }}
            </span>
            <span v-else></span> -->
            <span>{{ t('columns') }}</span>

            <div class="flex gap-1 items-center ml-2">
              <ChevronDown class="h-4 w-4 opacity-50 text-current" />
            </div>
          </Button>
        </slot>
      </PopoverTrigger>
      <PopoverContent
        class="p-0 min-w-[--radix-popper-anchor-width] w-96"
        align="start"
        ref="content"
      >
        <div class="flex items-center border-b px-3 top-0 sticky">
          <Search class="mr-2 h-4 w-4 shrink-0 opacity-50" />
          <ListboxFilter
            v-model="filter"
            class="w-full outline-none py-2"
            auto-focus
          />
        </div>

        <ListboxContent
          class="max-h-[300px] p-1 overflow-y-auto overflow-x-hidden"
        >
          <p v-if="filter && !itemsFiltered.length" class="px-2 py-1.5 text-sm">
            {{ t('empty') }}
          </p>

          <ListboxVirtualizer
            v-slot="{ option }"
            :options="itemsFiltered"
            :text-content="(opt) => opt.value"
            :estimate-size="40"
          >
            <ListboxItem
              :value="option.id"
              :key="option.id"
              class="flex w-full cursor-default select-none items-center rounded-sm px-2 pl-8 py-2 outline-none data-[highlighted]:bg-accent data-[disabled]:pointer-events-none data-[disabled]:opacity-50"
            >
              <span
                class="absolute left-2 flex h-3.5 w-3.5 items-center justify-center"
              >
                <ListboxItemIndicator>
                  <Check class="ml-auto h-4 w-4" />
                </ListboxItemIndicator>
              </span>

              <template v-if="option.parent">
                <span>{{ option.parent }}</span>
                <span class="mx-0.5 text-muted-foreground">/</span>
              </template>

              <span class="line-clamp-1">{{ option.value }}</span>
            </ListboxItem>
          </ListboxVirtualizer>
        </ListboxContent>
      </PopoverContent>
    </ListboxRoot>
  </Popover>
</template>
