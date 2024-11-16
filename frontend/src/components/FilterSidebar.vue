<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible'
import { ScrollArea } from '@/components/ui/scroll-area'
import { useFetchQuery } from '@/composables/useQuery'
import { client } from '@/lib/client'
import { ChevronDown } from 'lucide-vue-next'
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const { data: categories } = useFetchQuery({
  load() {
    return client.GET('/api/categories')
  },
  immediate: true,
})

const { data: brands } = useFetchQuery({
  load() {
    return client.GET('/api/brands')
  },
  immediate: true,
})

const emit = defineEmits(['filter'])

const selectedCategories = ref<string[]>([])
const selectedBrands = ref<string[]>([])
const isCategoryOpen = ref(true)
const isBrandOpen = ref(true)
const isFilterVisible = ref(false)

watch([selectedCategories, selectedBrands], () => {
  emit('filter', {
    categories: selectedCategories.value,
    brands: selectedBrands.value,
  })
})

const toggleCategory = (checked: boolean, categoryId: string) => {
  if (checked) {
    selectedCategories.value.push(categoryId)
  } else {
    selectedCategories.value = selectedCategories.value.filter(
      (id) => id !== categoryId
    )
  }
  emit('filter', {
    categories: selectedCategories.value,
    brands: selectedBrands.value,
  })
}

const toggleBrand = (checked: boolean, brandId: string) => {
  if (checked) {
    selectedBrands.value.push(brandId)
  } else {
    selectedBrands.value = selectedBrands.value.filter((id) => id !== brandId)
  }
  emit('filter', {
    categories: selectedCategories.value,
    brands: selectedBrands.value,
  })
}

const clearFilters = () => {
  selectedCategories.value = []
  selectedBrands.value = []
  emit('filter', {
    categories: selectedCategories.value,
    brands: selectedBrands.value,
  })
}

const toggleFilterVisibility = () => {
  isFilterVisible.value = !isFilterVisible.value
}
</script>

<template>
  <div>
    <div class="relative">
      <Button
        variant="ghost"
        size="sm"
        @click="toggleFilterVisibility"
        class="text-sm fixed top-13 right-4 z-50 lg:hidden"
      >
        Filters
      </Button>
      <div
        :class="[
          'w-64 bg-card rounded-lg border p-4 fixed top-0 left-0 h-full z-40 transition-transform transform',
          isFilterVisible ? 'translate-x-0' : '-translate-x-full',
          'lg:relative lg:translate-x-0 lg:h-auto lg:top-auto lg:left-auto lg:z-auto',
        ]"
      >
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-lg font-semibold">Filters</h2>
          <Button
            variant="ghost"
            size="sm"
            @click="clearFilters"
            class="text-sm"
          >
            Clear all
          </Button>
        </div>

        <Collapsible v-model:open="isCategoryOpen" class="space-y-2">
          <CollapsibleTrigger
            class="flex w-full justify-between items-center rounded-lg bg-secondary p-4 text-sm font-medium hover:bg-secondary/80"
          >
            {{ t('categories') }}
            <ChevronDown
              :class="isCategoryOpen ? 'rotate-180 transform' : ''"
              class="h-4 w-4 transition-transform duration-200"
            />
          </CollapsibleTrigger>
          <CollapsibleContent>
            <ScrollArea class="h-[200px] px-1">
              <div class="space-y-4 p-4">
                <div
                  v-for="category in categories"
                  :key="category.id"
                  class="flex items-center space-x-2"
                >
                  <Checkbox
                    :id="`category-${category.id}`"
                    :checked="selectedCategories.includes(category.id)"
                    @update:checked="
                      (checked) => toggleCategory(checked, category.id)
                    "
                  />
                  <label
                    :for="`category-${category.id}`"
                    class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    {{ category.name }}
                  </label>
                </div>
              </div>
            </ScrollArea>
          </CollapsibleContent>
        </Collapsible>

        <Collapsible v-model:open="isBrandOpen" class="space-y-2 mt-4">
          <CollapsibleTrigger
            class="flex w-full justify-between items-center rounded-lg bg-secondary p-4 text-sm font-medium hover:bg-secondary/80"
          >
            {{ t('brands') }}
            <ChevronDown
              :class="isBrandOpen ? 'rotate-180 transform' : ''"
              class="h-4 w-4 transition-transform duration-200"
            />
          </CollapsibleTrigger>
          <CollapsibleContent>
            <ScrollArea class="h-[200px] px-1">
              <div class="space-y-4 p-4">
                <div
                  v-for="brand in brands"
                  :key="brand.id"
                  class="flex items-center space-x-2"
                >
                  <Checkbox
                    :id="`brand-${brand.id}`"
                    :checked="selectedBrands.includes(brand.id)"
                    @update:checked="
                      (checked) => toggleBrand(checked, brand.id)
                    "
                  />
                  <label
                    :for="`brand-${brand.id}`"
                    class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
                  >
                    {{ brand.name }}
                  </label>
                </div>
              </div>
            </ScrollArea>
          </CollapsibleContent>
        </Collapsible>
      </div>
    </div>
  </div>
</template>
