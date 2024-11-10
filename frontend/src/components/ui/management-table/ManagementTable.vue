<template>
  <div class="overflow-x-auto">
    <div class="flex items-center justify-between my-4">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search..."
        class="p-2 border border-gray-300 rounded"
      />
      <div class="px-2 space-x-2">
        <Button v-if="secondTableAction" @click="secondTableAction">
          {{ sencondTableActionLabel }}
        </Button>
        <Button v-if="createAction" @click="createAction">
          {{ t('create') }}
        </Button>
      </div>
    </div>

    <table class="min-w-full">
      <thead>
        <tr>
          <th
            v-for="(header, index) in headers"
            :key="index"
            class="py-2 px-4 border-b border-gray-200 text-sm font-medium text-gray-600 text-left"
          >
            {{ header.title }}
          </th>
          <th
            v-if="onAction"
            class="py-2 px-4 border-b border-gray-200 text-sm font-medium text-gray-600 text-left"
          ></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, rowIndex) in paginatedData" :key="rowIndex">
          <td
            v-for="(header, colIndex) in headers"
            :key="colIndex"
            class="py-2 px-4 border-b border-gray-200 text-sm text-gray-600"
          >
            <template v-if="colIndex === 0 && redirect">
              <RouterLink
                :to="getRedirectLink(row)"
                class="text-primary underline"
              >
                <span v-if="header.mapFunction">
                  {{ header.mapFunction(getNestedValue(row, header.value)) }}
                </span>
                <span v-else>
                  {{ getNestedValue(row, header.value) }}
                </span>
              </RouterLink>
            </template>
            <template v-else-if="colIndex === 0 && secondaryNameAction">
              <span
                class="text-primary underline"
                @click="secondaryNameAction(row)"
              >
                <span v-if="header.mapFunction">
                  {{ header.mapFunction(getNestedValue(row, header.value)) }}
                </span>
                <span v-else>
                  {{ getNestedValue(row, header.value) }}
                </span>
              </span>
            </template>

            <template v-else>
              <span v-if="header.mapFunction">
                {{ header.mapFunction(getNestedValue(row, header.value)) }}
              </span>
              <span v-else>
                {{ getNestedValue(row, header.value) }}
              </span>
            </template>
          </td>
          <td
            v-if="onAction"
            class="py-2 px-4 border-b border-gray-200 text-sm text-end"
          >
            <Button
              @click="onAction(row)"
              variant="link"
              class="text-primary"
              :disabled="row.editable === false"
            >
              <span class="sr-only">Go to first page</span>
              <Trash class="w-4 h-4" />
            </Button>
          </td>
        </tr>
      </tbody>
    </table>

    <div class="flex items-center justify-between px-2 mt-4">
      <div></div>
      <div class="flex items-center space-x-6 lg:space-x-8">
        <div class="flex items-center space-x-2">
          <p class="text-sm font-medium">{{ t('rowsPerPage') }}</p>
          <Select
            :model-value="`${rowsPerPage}`"
            @update:model-value="updatePageSize"
          >
            <SelectTrigger class="h-8 w-[70px]">
              <SelectValue :placeholder="`${rowsPerPage}`" />
            </SelectTrigger>
            <SelectContent side="top">
              <SelectItem
                v-for="pageSize in [10, 20, 30, 40, 50]"
                :key="pageSize"
                :value="`${pageSize}`"
              >
                {{ pageSize }}
              </SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div
          class="flex w-[100px] items-center justify-center text-sm font-medium"
        >
          {{
            t('rowsPage', {
              current: currentPage,
              all: totalPages,
            })
          }}
        </div>
        <div class="flex items-center space-x-2">
          <Button
            variant="outline"
            class="w-8 h-8 p-0 lg:flex"
            :disabled="currentPage === 1"
            @click="firstPage"
          >
            <span class="sr-only">Go to first page</span>
            <ChevronsLeft class="w-4 h-4" />
          </Button>
          <Button
            variant="outline"
            class="w-8 h-8 p-0"
            :disabled="currentPage === 1"
            @click="previousPage"
          >
            <span class="sr-only">Go to previous page</span>
            <ChevronLeft class="w-4 h-4" />
          </Button>
          <Button
            variant="outline"
            class="w-8 h-8 p-0"
            :disabled="currentPage === totalPages"
            @click="nextPage"
          >
            <span class="sr-only">Go to next page</span>
            <ChevronRight class="w-4 h-4" />
          </Button>
          <Button
            variant="outline"
            class="w-8 h-8 p-0 lg:flex"
            :disabled="currentPage === totalPages"
            @click="lastPage"
          >
            <span class="sr-only">Go to last page</span>
            <ChevronsRight class="w-4 h-4" />
          </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { ref, computed, watch } from 'vue'
import {
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight,
  Trash,
} from 'lucide-vue-next'

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

interface Header {
  title: string
  value: string
  mapFunction?: (value: any) => any
}

interface RowData {
  [key: string]: any
}

const props = defineProps<{
  headers: Header[]
  data: RowData[]
  onAction?: (row: RowData) => void
  createAction?: () => void
  redirect?: string
  redirectKey?: string
  secondaryNameAction?: (row: RowData) => void
  secondTableAction?: () => void
  sencondTableActionLabel?: string
}>()

const searchQuery = ref<string>('')
const rowsPerPage = ref<number>(10)
const currentPage = ref<number>(1)
const rowsPerPageOptions = ref<number[]>([5, 10, 15, 25, 50])

const filteredData = computed(() => {
  if (!searchQuery.value) {
    return props.data
  }
  return props.data.filter((row) => {
    return Object.values(row).some((value) =>
      String(value).toLowerCase().includes(searchQuery.value.toLowerCase()),
    )
  })
})

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * rowsPerPage.value
  const end = start + rowsPerPage.value
  return filteredData.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(filteredData.value.length / rowsPerPage.value)
})

const getNestedValue = (obj: RowData, path: string) => {
  return path
    .split('.')
    .reduce((acc: any, part: string) => acc && acc[part], obj)
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value += 1
  }
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value -= 1
  }
}

const firstPage = () => {
  currentPage.value = 1
}

const lastPage = () => {
  currentPage.value = totalPages.value
}

function updatePageSize(value: string) {
  const pageSize = parseInt(value, 10)

  if (isNaN(pageSize)) {
    return
  }

  rowsPerPage.value = pageSize
}

function getRedirectLink(row: any) {
  var lastFragment = row[props.redirectKey ?? 'attribute_id']

  return `${props.redirect}/${lastFragment}`
}

watch([searchQuery, rowsPerPage], () => {
  currentPage.value = 1
})
</script>
