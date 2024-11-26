<template>
    <div>
      <AdminNavBar />
      <div class="container mx-auto p-4">
        <div v-if="brand" class="bg-white shadow-md rounded-lg p-6">
          <h1 class="text-3xl font-semibold mb-4">{{ brand.name }}</h1>
          <img :src="brand.photo ?? ''" alt="brand photo" class="w-full h-64 object-cover rounded-lg mb-4" />
          <p class="text-gray-700 mb-4">{{ brand.description }}</p>
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
  
  const route = useRoute('/admin/brands/[id]')
  
  const { data: brand } = useFetchQuery({
    load() {
      return client.GET(`/api/brands/{brand_id}`, {
        params: {
          path: {
            brand_id: route.params.id as string
          }
      }
        })
    },
    immediate: true,
  })
  
  </script>
  
  <style scoped>
  .container {
    max-width: 1200px;
  }
  </style>