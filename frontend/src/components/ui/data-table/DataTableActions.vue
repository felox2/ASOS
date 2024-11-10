<script setup lang="ts">
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Row } from '@tanstack/vue-table'
import { MoreHorizontal } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import { DataTableAction } from '.'

const { t } = useI18n()

defineProps<{
  row: Row<any>
  actions: DataTableAction[]
}>()
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger as-child>
      <Button variant="ghost" class="w-6 h-6 p-0">
        <span class="sr-only">Open menu</span>
        <MoreHorizontal class="w-4 h-4" />
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent align="center">
      <DropdownMenuLabel>{{ t('actions') }}</DropdownMenuLabel>
      <DropdownMenuSeparator />

      <DropdownMenuItem v-for="action in actions" @click="action.handler(row)">
        {{ action.label }}
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
