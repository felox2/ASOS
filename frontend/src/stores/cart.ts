import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useCartStore = defineStore('store', () => {
  const items = ref([])

  const count = computed(() => 6)
  const total = computed(() => 0)

  return { items, count, total }
})
