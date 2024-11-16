<script setup lang="ts">
import { useCartStore } from '@/stores/cart'
import { computed, defineProps } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import { Button } from './ui/button'
import { Card } from './ui/card'

const { t, n } = useI18n()

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
const cartStore = useCartStore()

const cartItem = computed(() => cartStore.getCartItem(props.product.id))

function addToCart() {
  cartStore.addCartItem({
    product_id: props.product.id,
    // @ts-ignore
    product: props.product,
    quantity: 1,
  })
}
</script>

<template>
  <Card class="max-w-xs w-full mx-auto p-4">
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
      <p class="text-muted-foreground">{{ product.description }}</p>
      <p class="text-muted-foreground">Stock: {{ product.stock_quantity }}</p>
      <!-- <p class="text-gray-900 font-bold text-right">
        Price: ${{ product.price }}
      </p> -->
    </RouterLink>

    <div class="flex items-center justify-between mt-2">
      <div class="font-semibold text-lg">
        {{ n(product.price, 'currency') }}
      </div>

      <!-- TODO: show item is in cart -->
      <Button @click="addToCart">
        {{ cartItem ? t('addAnother') : t('toCart') }}
      </Button>
    </div>
  </Card>
</template>

<style scoped>
.product-photo-container {
  height: 192px;
}

.brand-photo-container {
  width: 48px;
  height: 48px;
}
</style>
