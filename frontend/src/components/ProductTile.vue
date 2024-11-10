<template>
    <div class="product-tile border border-gray-300 p-4 rounded-lg max-w-xs mx-auto">
      <RouterLink :to="`/products/${product.id}`" class="block">
        <div class="product-photo-container w-full h-48 bg-gray-200 rounded-lg flex items-center justify-center">
          <img v-if="product.photo" :src="product.photo" alt="Product photo" class="product-photo w-full h-full object-cover rounded-lg" />
          <span v-else class="text-gray-500">No Image Available</span>
        </div>
        <h2 class="text-xl font-semibold mt-4">{{ product.name }}</h2>
        <p class="text-gray-700">{{ product.description }}</p>
        <p class="text-gray-900 font-bold">Price: ${{ product.price }}</p>
        <p class="text-gray-700">Stock: {{ product.stock_quantity }}</p>
        <div class="brand-info flex items-center mt-4">
          <div class="brand-photo-container w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center mr-4">
            <img v-if="product?.brand?.photo" :src="product.brand.photo" alt="Brand photo" class="brand-photo w-full h-full object-cover rounded-full" />
            <span v-else class="text-gray-500">No Image</span>
          </div>
          <p class="text-gray-900">{{ product.brand?.name }}</p>
        </div>
      </RouterLink>
      <Button class="ml-auto mt-4">{{ t('toCart') }}</Button>
    </div>
  </template>
  
  <script setup lang="ts">
  import { defineProps } from 'vue'
  import { RouterLink } from 'vue-router'
  import { Button } from './ui/button'
  import { useI18n } from 'vue-i18n'
  
  const { t } = useI18n();
  
  interface Brand {
    id: string;
    name: string;
    description?: string | null;
    photo?: string | null;
  }
  
  interface Product {
    name: string;
    description?: string | null;
    price: number;
    stock_quantity?: number | null;
    photo?: string | null;
    brand_id?: string | null;
    id: string;
    created_at: string;
    modified_at: string;
    brand?: Brand | null;
    additional_photos: string[];
  }
  
  const props = defineProps<{ product: Product }>();
  </script>
  
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