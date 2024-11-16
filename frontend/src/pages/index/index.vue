<script setup lang="ts">
import ProductTile from '@/components/ProductTile.vue'
import { Button } from '@/components/ui/button'
import { Card, CardContent } from '@/components/ui/card'
import { client } from '@/lib/client'
import { useFetchQuery } from '@/lib/useQuery'
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import FilterSidebar from '@/components/FilterSidebar.vue' 

const { t } = useI18n()
const pageSize = 12

const selectedFilters = ref<{ categories: string[], brands: string[] }>({
  categories: [],
  brands: []
})

const { data: products, reload: reloadProducts } = useFetchQuery({
  load() {
    return client.GET('/api/products', {
      params: {
        query: {
          page_size: pageSize,
          category_ids: selectedFilters.value.categories,
          brand_ids: selectedFilters.value.brands,
        },
      },
    })
  },
  immediate: true,
})

const disabled = ref(false)

watch(products, (newProducts) => {
  if ((newProducts?.length ?? 0) % pageSize !== 0) {
    disabled.value = true
  } else {
    disabled.value = false
  }
})

const loadMore = async () => {
  if (!products.value) return
  const response = await client.GET('/api/products', {
    params: {
      query: {
        page: Math.ceil(products.value.length / pageSize) + 1,
        page_size: pageSize,
        categories: selectedFilters.value.categories,
        brands: selectedFilters.value.brands,
      },
    },
  })

  if (!response.data) return

  products.value = [...products.value, ...response.data]
}

const handleFilter = async ({ categories, brands }: { categories: string[], brands: string[] }) => {
  console.log(categories, brands)
  selectedFilters.value = { categories, brands }
  products.value = [] 
  await reloadProducts() 
}
</script>

<template>
  <div class="container mx-auto p-4">
    <div class="flex gap-6">
      <FilterSidebar
        @filter="handleFilter"

      />
      
      <Card class="flex-1">
        <CardContent class="p-6">
          <div class="flex justify-center">
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              <ProductTile
                v-for="product in products"
                :key="product.id"
                :product="product"
              />
            </div>
          </div>
          <div class="flex justify-center">
            <Button v-if="!disabled" @click="loadMore" class="mt-4">
              {{ t('loadMore') }}
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>