<template>
    <div>
      <AdminNavBar />
      <div class="container mx-auto p-4">
        <div v-if="product" class="bg-white shadow-md rounded-lg p-6">
          <h1 class="text-3xl font-semibold mb-4">{{ product.name }}</h1>
          <img :src="product.photo ?? ''" alt="Product photo" class="w-full h-64 object-cover rounded-lg mb-4" />
          <p class="text-gray-700 mb-4">{{ product.description }}</p>
          <p class="text-gray-900 font-bold mb-4">Price: ${{ product.price }}</p>
          <p class="text-gray-700 mb-4">Stock: {{ product.stock_quantity }}</p>
          <div class="brand-info flex items-center mb-6">
            <div class="brand-photo-container w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mr-4">
              <img v-if="product.brand?.photo" :src="product.brand.photo" alt="Brand photo" class="brand-photo w-full h-full object-cover rounded-full" />
              <span v-else class="text-gray-500">No Image</span>
            </div>
            <div>
              <p class="text-gray-900 font-semibold">{{ product.brand?.name }}</p>
              <p class="text-gray-700">{{ product.brand?.description }}</p>
            </div>
          </div>
        </div>
        <div v-else class="text-center text-gray-500">Loading...</div>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import AdminNavBar from '@/components/AdminNavBar.vue'
  import { client } from '@/lib/client'
  import { useFetchQuery } from '@/lib/useQuery'

  const route = useRoute('/admin/products/[id]')
  
  

  const {data: product } = useFetchQuery({
    load() {
      return client.GET(`/api/products/{product_id}`, {
        params: {
            path: {
                product_id: route.params.id as string
            }
        },
      })
    },
    immediate: true,
  })
  
  </script>
  
  <style scoped>
  .container {
    max-width: 1200px;
  }
  
  .brand-photo-container {
    width: 64px;
    height: 64px;
  }
  </style>