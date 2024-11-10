<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import type { Column } from '@tanstack/vue-table'
import { ArrowDownAZ, ArrowDownZA, ArrowUpDown } from 'lucide-vue-next'

interface DataTableColumnHeaderProps {
  column: Column<any, any>
  title: string
}

defineProps<DataTableColumnHeaderProps>()
</script>

<script lang="ts">
export default {
  inheritAttrs: false,
}
</script>

<template>
  <div
    v-if="column.getCanSort()"
    :class="cn('flex items-center space-x-2', $attrs.class ?? '')"
  >
    <Button
      variant="ghost"
      size="sm"
      class="-ml-3 h-8 font-medium text-sm"
      @click="column.toggleSorting()"
    >
      <span>{{ title }}</span>
      <ArrowDownAZ v-if="column.getIsSorted() === 'asc'" class="w-4 h-4 ml-2" />
      <ArrowDownZA
        v-else-if="column.getIsSorted() === 'desc'"
        class="w-4 h-4 ml-2"
      />
      <ArrowUpDown v-else class="w-4 h-4 ml-2" />
    </Button>
  </div>

  <div v-else :class="$attrs.class">
    {{ title }}
  </div>
</template>
