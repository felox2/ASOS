<script setup lang="ts">
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { cn } from '@/lib/utils'
import { onClickOutside } from '@vueuse/core'
import { Check, ChevronDown, Search, X } from 'lucide-vue-next'
import {
  ListboxContent,
  ListboxFilter,
  ListboxItem,
  ListboxItemIndicator,
  ListboxRoot,
  ListboxVirtualizer,
} from 'radix-vue'
import { type HTMLAttributes, computed, onMounted, ref } from 'vue'
import { Button } from '../button'

interface Item {
  id: string
  value: string
}

interface Props {
  items: Item[]
  placeholder?: string
  placeholderInput?: string
  empty?: string
  class?: HTMLAttributes['class']
  hideFilter?: boolean
  multiple?: boolean
}

defineOptions({
  inheritAttrs: false,
})

const props = defineProps<Props>()
const modelValue = defineModel<string | string[] | undefined>()
const open = ref(false)
const filter = ref('')
const content = ref()

const hasValue = computed(() =>
  props.multiple ? !!modelValue.value?.length : !!modelValue.value,
)
const valueLabel = computed(() => {
  if (!props.multiple) {
    return props.items.find((item) => item.id === modelValue.value)?.value
  }

  return props.items
    .filter((item) => modelValue.value?.includes(item.id))
    .map((item) => item.value)
    .join(', ')
})

function normalize(str: string) {
  return str
    .toLowerCase()
    .normalize('NFD')
    .replace(/\p{Diacritic}/gu, '')
}

const valuesNormalized = computed(() =>
  props.items.map((i) => normalize(i.value)),
)

const itemsFiltered = computed(() => {
  const query = filter.value ? normalize(filter.value) : filter.value

  if (!query) {
    return props.items
  }

  const filtered: Item[] = []

  for (let i = 0; i < props.items.length; i++) {
    const v = valuesNormalized.value[i]

    if (v.includes(query)) {
      filtered.push(props.items[i])
    }
  }

  return filtered
})

function close() {
  open.value = false
}

function handleSelect(value: any) {
  if (value && !props.multiple) {
    close()
  }
}

function clear(e: MouseEvent) {
  e.stopPropagation()

  modelValue.value = props.multiple ? [] : undefined
  open.value = false
}

onMounted(() => {
  onClickOutside(content.value.$el, () => {
    if (open.value && !props.multiple) {
      open.value = false
    }
  })
})
</script>

<template>
  <Popover v-model:open="open">
    <ListboxRoot
      v-model="modelValue"
      @update:modelValue="handleSelect"
      :multiple="multiple"
    >
      <PopoverTrigger as-child>
        <slot name="trigger">
          <Button
            v-bind="$attrs"
            variant="outline"
            role="combobox"
            :aria-expanded="open"
            :class="
              cn(
                'flex text-base h-12 font-normal min-w-40 w-full items-center justify-between shadow-sm border border-input rounded-md bg-background px-3 py-2 focus:outline-none disabled:opacity-100 disabled:cursor-not-allowed disabled:bg-light-gray disabled:border-dark-gray disabled:placeholder:text-muted-gray [&>span]:line-clamp-1 text-black relative group aria-invalid:border-red aria-invalid:bg-light-red aria-invalid:text-red aria-invalid:focus-visible:bg-background aria-invalid:focus-visible:text-black aria-invalid:focus-visible:placeholder:text-black/25 aria-invalid:focus-visible:shadow-light-red',
                props.class,
              )
            "
          >
            <span
              :data-open="open || hasValue ? 'true' : undefined"
              :data-value="hasValue ? 'true' : undefined"
              class="text-muted-foreground origin-top-left transition-transform data-[value]:absolute data-[open]:scale-75 data-[open]:-translate-y-3 group-aria-invalid:text-red"
            >
              {{ placeholder ?? '' }}
            </span>
            <span v-if="valueLabel" class="mt-2">
              {{ valueLabel }}
            </span>
            <span v-else></span>

            <div class="flex gap-1 items-center ml-2">
              <Button
                v-if="hasValue"
                @click="clear"
                variant="ghost"
                class="p-0 h-5 text-current hover:bg-transparent hover:text-current"
              >
                <X class="size-5" />
              </Button>
              <ChevronDown class="h-4 w-4 opacity-50 text-current" />
            </div>
          </Button>
        </slot>
      </PopoverTrigger>
      <PopoverContent
        class="p-0 min-w-[--radix-popper-anchor-width]"
        align="start"
        ref="content"
      >
        <div
          v-if="!hideFilter"
          class="flex items-center border-b px-3 top-0 sticky"
        >
          <Search class="mr-2 h-4 w-4 shrink-0 opacity-50" />
          <ListboxFilter
            v-model="filter"
            class="w-full outline-none py-2"
            auto-focus
            :placeholder="placeholderInput"
          />
        </div>

        <ListboxContent
          class="max-h-[300px] p-1 overflow-y-auto overflow-x-hidden"
        >
          <slot name="filtered" v-if="filter && !itemsFiltered.length">
            <p class="px-2 py-1.5 text-sm">
              {{ empty }}
            </p>
          </slot>
          <slot name="empty" v-if="!filter && !itemsFiltered.length">
            <p class="px-2 py-1.5 text-sm">
              {{ empty }}
            </p>
          </slot>

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

              <span>{{ option.value }}</span>
            </ListboxItem>
          </ListboxVirtualizer>
        </ListboxContent>
      </PopoverContent>
    </ListboxRoot>
  </Popover>
</template>
