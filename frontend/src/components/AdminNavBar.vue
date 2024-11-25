<template>
    <div>
      <nav class="bg-gray-800 p-4">
        <div class="container mx-auto flex justify-between items-center">
          <div class="flex space-x-4">
            <router-link to="/admin/products" class="text-white hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">
              Products
            </router-link>
            <router-link to="/admin/categories" class="text-white hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">
              Categories
            </router-link>
            <router-link to="/admin/brands" class="text-white hover:bg-gray-700 px-3 py-2 rounded-md text-sm font-medium">
              Brands
            </router-link>
          </div>
        </div>
      </nav>
      <div class="container mx-auto p-4">
        <router-view />
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  </script>
  