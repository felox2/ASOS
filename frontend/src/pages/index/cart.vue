<script setup lang="ts">
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import {
  NumberField,
  NumberFieldContent,
  NumberFieldDecrement,
  NumberFieldIncrement,
  NumberFieldInput,
} from '@/components/ui/number-field'
import { client } from '@/lib/client'
import { useCartStore } from '@/stores/cart'
import { X } from 'lucide-vue-next'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

const router = useRouter()

const { t, n } = useI18n()
const cartStore = useCartStore()

function updateItemQuantity(item: any, quantity: number) {
  console.log(quantity)

  cartStore.updateCartItem({
    ...item,
    quantity,
  })
}

function order() {
  client.POST('/api/cart/order').then((res) => {
    cartStore.clear()
    router.push('/thanks')
  }).catch((err) => {
    console.error(err)
  })
}

</script>

<template>
  <div class="max-w-6xl mx-auto">
    <Card>
      <CardHeader>
        <CardTitle>{{ t('cart') }}</CardTitle>
      </CardHeader>
      <CardContent>
        <div>
          <div
            v-for="item in cartStore.items"
            class="flex gap-3 border-b py-2.5"
          >
            <img
              v-if="item.product?.photo"
              class="size-20 rounded aspect-square"
              :src="item.product?.photo"
            />

            <div class="flex flex-col justify-between w-full gap-1">
              <div class="flex justify-between w-full">
                <RouterLink
                  :to="{
                    name: '//products/[id]',
                    params: { id: item.product_id },
                  }"
                >
                  <h4 class="text-lg">{{ item.product?.name }}</h4>
                </RouterLink>
                <Button
                  class="p-0 size-5"
                  variant="ghost"
                  @click="cartStore.removeCartItem(item)"
                >
                  <X class="size-4" />
                </Button>
              </div>
              <div class="flex justify-between items-center w-full">
                <NumberField
                  class="w-24"
                  :min="1"
                  :model-value="item.quantity"
                  @update:model-value="updateItemQuantity(item, $event)"
                >
                  <NumberFieldContent>
                    <NumberFieldDecrement />
                    <NumberFieldInput />
                    <NumberFieldIncrement />
                  </NumberFieldContent>
                </NumberField>

                <span>{{ n(item.product?.price || 0, 'currency') }}</span>
              </div>
            </div>
          </div>

          <div class="flex ml-auto max-w-56 justify-between mt-2">
            <span>{{ t('total') }}</span>
            <span class="font-semibold">
              {{ n(cartStore.total, 'currency') }}
            </span>
          </div>
        </div>
      </CardContent>
      <CardFooter class="flex justify-end">
        <Button :disabled="cartStore.count === 0" @click="order">
              {{ t('checkout') }}
        </Button>
      </CardFooter>
    </Card>
  </div>
</template>
