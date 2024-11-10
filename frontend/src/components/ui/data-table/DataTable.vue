<script setup lang="ts" generic="TData, TValue">
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'
import { valueUpdater } from '@/lib/utils'
import type {
  ColumnDef,
  ColumnFiltersState,
  SortingState,
  VisibilityState,
} from '@tanstack/vue-table'
import {
  ColumnPinningState,
  FlexRender,
  getCoreRowModel,
  PaginationState,
  useVueTable,
} from '@tanstack/vue-table'
import { ref } from 'vue'
import DataTableColumnVisibility from './DataTableColumnVisibility.vue'
import DataTablePagination from './DataTablePagination.vue'

const props = defineProps<{
  columns: ColumnDef<TData, TValue>[]
  data: TData[]

  rowCount?: number
}>()

const columnFilters = defineModel<ColumnFiltersState>('filters', {
  default: () => [],
})
const columnVisibility = defineModel<VisibilityState>('visibility', {
  default: () => ({}),
})
const sorting = defineModel<SortingState>('sorting', {
  default: () => [],
})
const pagination = defineModel<PaginationState>('pagination', {
  default: () => ({
    pageIndex: 0,
    pageSize: 5,
  }),
})

const rowSelection = ref({})
// const columnVisibility = ref<VisibilityState>({})
const columnPinning = ref<ColumnPinningState>({
  left: ['select'],
  right: ['actions'],
})
const columnOrder = ref<string[]>([])

const table = useVueTable({
  manualPagination: true,
  manualSorting: true,
  manualFiltering: true,

  get data() {
    return props.data
  },
  get columns() {
    return props.columns
  },
  get rowCount() {
    return props.rowCount ?? 1
  },

  getCoreRowModel: getCoreRowModel(),
  onRowSelectionChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, rowSelection),
  onColumnVisibilityChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, columnVisibility),

  onSortingChange: (updaterOrValue) => valueUpdater(updaterOrValue, sorting),
  onPaginationChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, pagination),
  onColumnFiltersChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, columnFilters),
  onColumnOrderChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, columnOrder),
  onColumnPinningChange: (updaterOrValue) =>
    valueUpdater(updaterOrValue, columnPinning),

  state: {
    get rowSelection() {
      return rowSelection.value
    },
    get sorting() {
      return sorting.value
    },
    get columnVisibility() {
      return columnVisibility.value
    },
    get pagination() {
      return pagination.value
    },
    get columnFilters() {
      return columnFilters.value
    },
    get columnOrder() {
      return columnOrder.value
    },
    get columnPinning() {
      return columnPinning.value
    },
  },
})
</script>

<template>
  <div>
    <div class="flex items-center justify-between my-4">
      <div class="flex gap-2">
        <slot
          name="actions"
          :selected-rows="table.getSelectedRowModel().rows"
          :row-selected="
            table.getIsSomeRowsSelected() || table.getIsAllRowsSelected()
          "
          :clear-selection="table.resetRowSelection"
        ></slot>
      </div>

      <div class="flex">
        <DataTableColumnVisibility :table="table" />
      </div>
    </div>

    <Table>
      <TableHeader>
        <TableRow
          v-for="headerGroup in table.getHeaderGroups()"
          :key="headerGroup.id"
        >
          <TableHead v-for="header in headerGroup.headers" :key="header.id">
            <FlexRender
              v-if="!header.isPlaceholder"
              :render="header.column.columnDef.header"
              :props="header.getContext()"
            />
          </TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        <template v-if="table.getRowModel().rows?.length">
          <TableRow
            v-for="row in table.getRowModel().rows"
            :key="row.id"
            :data-state="row.getIsSelected() ? 'selected' : undefined"
          >
            <TableCell v-for="cell in row.getVisibleCells()" :key="cell.id">
              <FlexRender
                :render="cell.column.columnDef.cell"
                :props="cell.getContext()"
              />
            </TableCell>
          </TableRow>
        </template>
        <template v-else>
          <TableRow>
            <TableCell :colspan="columns.length" class="h-24 text-center">
              No results.
            </TableCell>
          </TableRow>
        </template>
      </TableBody>
    </Table>

    <DataTablePagination :table="table" class="mt-2" />
  </div>
</template>
