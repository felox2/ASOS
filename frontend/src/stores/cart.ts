import { client } from '@/lib/client'
import type { components } from '@/types/api'
import { defineStore } from 'pinia'
import { computed, onMounted, ref } from 'vue'

type CartItem = components['schemas']['CartItemRead']

export const useCartStore = defineStore('store', () => {
  const items = ref<CartItem[]>([])

  const count = computed(() => items.value.length)
  const total = computed(() =>
    items.value.reduce(
      (acc, x) => acc + (x.product?.price ?? 0) * x.quantity,
      0
    )
  )

  function getCartItem(product_id: string) {
    return items.value.find((x) => x.product_id === product_id)
  }

  async function removeCartItem(item: CartItem) {
    const index = items.value.findIndex((x) => x.product_id === item.product_id)
    if (index !== -1) {
      items.value.splice(index, 1)
    }

    await client.POST('/api/cart/items', {
      // @ts-ignore
      body: {
        product_id: item.product_id,
        quantity: 0,
      },
    })
  }

  async function addCartItem(item: CartItem) {
    const existingItem = items.value.find(
      (x) => x.product_id === item.product_id
    )
    if (!existingItem) {
      items.value.push(item)

      await client.POST('/api/cart/items', {
        // @ts-ignore
        body: {
          product_id: item.product_id,
          quantity: item.quantity,
        },
      })
      return
    }

    existingItem.quantity++

    await client.POST('/api/cart/items', {
      // @ts-ignore
      body: {
        product_id: existingItem.product_id,
        quantity: existingItem.quantity,
      },
    })
  }

  async function updateCartItem(item: CartItem) {
    const existingItem = items.value.find(
      (x) => x.product_id === item.product_id
    )
    if (!existingItem) {
      await addCartItem(item)
      return
    }

    existingItem.quantity = item.quantity

    await client.POST('/api/cart/items', {
      // @ts-ignore
      body: {
        product_id: existingItem.product_id,
        quantity: existingItem.quantity,
      },
    })
  }

  onMounted(async () => {
    const { data } = await client.GET('/api/cart')
    if (!data) {
      return
    }

    items.value = data.items
  })

  async function clear() {
    const { data } = await client.GET('/api/cart')
    if (!data) {
      return
    }

    items.value = data.items
  }

  return {
    items,
    count,
    total,
    getCartItem,
    addCartItem,
    updateCartItem,
    removeCartItem,
    clear
  }
})
