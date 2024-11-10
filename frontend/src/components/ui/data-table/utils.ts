import { ColumnDef, createColumnHelper, Row } from '@tanstack/vue-table'
import { intlFormat, intlFormatDistance } from 'date-fns'
import { h, VNode } from 'vue'
import { DataTableAction, DataTableColumnHeader, DataTableHoverCard } from '.'
import { Checkbox } from '../checkbox'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '../tooltip'
import DataTableActions from './DataTableActions.vue'

const helper = createColumnHelper<any>()

export function createStateColumn(t: (key: string) => string) {
  return helper.accessor('entity_statemachine_state_name', {
    id: '$."entity_statemachine_state_name"',
    enableHiding: false,
    header: ({ column }) =>
      h(DataTableColumnHeader, {
        column,
        title: t('state'),
      }),
    cell: ({ row }) =>
      h('span', t(row.original.entity_statemachine_state_name)),
  })
}

export function createSelectColumn() {
  return helper.display({
    id: 'select',
    enableHiding: false,
    enableSorting: false,
    header: ({ table }) =>
      h('div', { class: 'flex' }, [
        h(Checkbox, {
          checked: table.getIsAllPageRowsSelected(),
          'onUpdate:checked': (value: boolean) =>
            table.toggleAllPageRowsSelected(!!value),
        }),
      ]),
    cell: ({ row }) =>
      h('div', { class: 'flex' }, [
        h(Checkbox, {
          checked: row.getIsSelected(),
          'onUpdate:checked': (value: boolean) => row.toggleSelected(!!value),
          ariaLabel: 'Select row',
        }),
      ]),
  })
}

export function createUpdatedAtColumn(
  t: (key: string) => string,
  locale: string,
) {
  return helper.accessor('entity_statemachine_state_created', {
    id: '$.entity_statemachine_state_created',
    meta: {
      attributeId: 'updated',
    },
    header: ({ column }) =>
      h(DataTableColumnHeader, {
        column,
        title: t('updated'),
      }),
    cell: ({ row }) => {
      // FIXME: fix in db
      const date = new Date(
        row.original.entity_statemachine_state_created + 'Z',
      )
      const formattedDistance = intlFormatDistance(date, new Date(), {
        locale,
      })
      const formattedDate = intlFormat(
        date,
        {
          dateStyle: 'full',
          timeStyle: 'short',
        },
        {
          locale,
        },
      )

      return h(TooltipProvider, {}, () => [
        h(Tooltip, {}, () => [
          h(TooltipTrigger, { asChild: true }, () => [
            h('span', {}, formattedDistance),
          ]),
          h(TooltipContent, {}, () => formattedDate),
        ]),
      ])
    },
  })
}

export function createCreatedAtColumn(
  t: (key: string) => string,
  locale: string,
) {
  return helper.accessor('created', {
    id: '$.created',
    meta: {
      attributeId: 'created',
    },
    header: ({ column }) =>
      h(DataTableColumnHeader, {
        column,
        title: t('created'),
      }),
    cell: ({ row }) => {
      const date = new Date(row.original.created)
      const formattedDistance = intlFormatDistance(date, new Date(), {
        locale,
      })
      const formattedDate = intlFormat(
        date,
        {
          dateStyle: 'full',
          timeStyle: 'short',
        },
        {
          locale,
        },
      )

      return h(TooltipProvider, {}, () => [
        h(Tooltip, {}, () => [
          h(TooltipTrigger, { asChild: true }, () => [
            h('span', {}, formattedDistance),
          ]),
          h(TooltipContent, {}, () => formattedDate),
        ]),
      ])
    },
  })
}

export function createActionsColumn(actions: DataTableAction[]) {
  return helper.display({
    id: 'actions',
    enableHiding: false,
    enableSorting: false,
    size: 10,
    cell: ({ row }) =>
      h('div', { class: 'text-right' }, [
        h(DataTableActions, {
          row,
          actions,
        }),
      ]),
  })
}

export function createHoverColumn(
  title: string,
  renderTrigger: (row: Row<any>) => VNode,
  renderContent: (row: Row<any>) => VNode,
) {
  return {
    id: title,
    header: ({ column }) =>
      h(DataTableColumnHeader, {
        column,
        title,
      }),
    cell: ({ row }) =>
      h(
        DataTableHoverCard,
        {},
        {
          trigger: () => renderTrigger(row),
          content: () => renderContent(row),
        },
      ),
  } as ColumnDef<any>
}
