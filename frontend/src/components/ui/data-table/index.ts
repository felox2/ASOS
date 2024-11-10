import { Row } from '@tanstack/vue-table'

export { default as DataTable } from './DataTable.vue'
export { default as DataTableColumnHeader } from './DataTableColumnHeader.vue'
export { default as DataTableHoverCard } from './DataTableHoverCard.vue'
export { default as DataTablePagination } from './DataTablePagination.vue'
export * from './utils.ts'

export interface DataTableAction {
  label: string
  handler: (row: Row<any>) => void
}
