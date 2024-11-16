<script setup lang="ts">
import { ref, watch } from 'vue'
import { ChevronDown } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from '@/components/ui/collapsible'
import { Checkbox } from '@/components/ui/checkbox'
import { ScrollArea } from '@/components/ui/scroll-area'
import { useFetchQuery } from '@/composables/useQuery'
import { client } from '@/lib/client'

const { data: categories } = useFetchQuery({
  load() {
    return client.GET('/api/categories')
  },
  immediate: true
})

const { data: brands } = useFetchQuery({
  load() {
    return client.GET('/api/brands')
  },
  immediate: true
})

const emit = defineEmits(['filter'])

const selectedCategories = ref<string[]>([])
const selectedBrands = ref<string[]>([])
const isCategoryOpen = ref(true)
const isBrandOpen = ref(true)

watch([selectedCategories, selectedBrands], () => {
  emit('filter', {
    categories: selectedCategories.value,
    brands: selectedBrands.value
  })
})

const toggleCategory = (checked: boolean, categoryId: string) => {
  if (checked) {
    selectedCategories.value.push(categoryId)
  } else {
    selectedCategories.value = selectedCategories.value.filter(id => id !== categoryId)
  }
  emit('filter', {
    categories: selectedCategories.value,
    brands: selectedBrands.value
  })
}

const toggleBrand = (checked: boolean, brandId: string) => {
  if (checked) {
    selectedBrands.value.push(brandId)
  } else {
    selectedBrands.value = selectedBrands.value.filter(id => id !== brandId)
  }
  emit('filter', {
    categories: selectedCategories.value,
    brands: selectedBrands.value
  })
}

const clearFilters = () => {
  selectedCategories.value = []
  selectedBrands.value = []
  emit('filter', {
    categories: selectedCategories.value,
    brands: selectedBrands.value
  })
}
</script>

<template>
  <div class="w-64 bg-white rounded-lg border p-4">
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
      <CollapsibleTrigger class="flex w-full justify-between items-center rounded-lg bg-secondary p-4 text-sm font-medium hover:bg-secondary/80">
        Categories
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
                @update:checked="(checked) => toggleCategory(checked, category.id)"
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
      <CollapsibleTrigger class="flex w-full justify-between items-center rounded-lg bg-secondary p-4 text-sm font-medium hover:bg-secondary/80">
        Brands
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
                @update:checked="(checked) => toggleBrand(checked, brand.id)"
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
</template>