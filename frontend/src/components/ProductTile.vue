<script setup lang="ts">
import { defineProps } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import { Button } from './ui/button'

const { t } = useI18n()

interface Brand {
  id: string
  name: string
  description?: string | null
  photo?: string | null
}

interface Product {
  name: string
  description?: string | null
  price: number
  stock_quantity?: number | null
  photo?: string | null
  brand_id?: string | null
  id: string
  created_at: string
  modified_at: string
  brand?: Brand | null
  additional_photos: string[]
}

const props = defineProps<{ product: Product }>()
</script>

<template>
  <div
    class="product-tile border border-gray-300 p-4 rounded-lg max-w-xs mx-auto"
  >
    <RouterLink :to="`/products/${product.id}`" class="block">
      <div
        class="product-photo-container w-full h-48 bg-gray-200 rounded-lg flex items-center justify-center"
      >
        <img
          v-if="product.photo"
          :src="product.photo"
          alt="Product photo"
          class="product-photo w-full h-full object-cover rounded-lg"
        />
        <span v-else class="text-gray-500">No Image Available</span>
      </div>
      <h2 class="text-xl font-semibold mt-4">{{ product.name }}</h2>
      <p class="text-gray-700">{{ product.description }}</p>
      <p class="text-gray-700">Stock: {{ product.stock_quantity }}</p>
      <p class="text-gray-900 font-bold text-right">Price: ${{ product.price }}</p>
      </RouterLink>
      <div class="flex justify-end">  
        <Button class="ml-auto mt-4">{{ t('toCart') }}</Button>
      </div>
  </div>
</template>

<style scoped>
.product-tile {
  margin: 16px;
}

.product-photo-container {
  height: 192px;
}

.brand-photo-container {
  width: 48px;
  height: 48px;
}
</style>
