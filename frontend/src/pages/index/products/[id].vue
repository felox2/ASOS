<template>
  <Card class="container mx-auto p-4 mt-10" v-if="product">
    <div
      class="product-detail max-w-4xl mx-auto rounded-lg p-6 grid grid-cols-1 lg:grid-cols-2 gap-6"
    >
      <div class="w-full sm:w-auto">
        <Carousel
          class="relative w-full max-w-xs"
          @init-api="(val) => (emblaMainApi = val)"
        >
          <CarouselContent>
            <CarouselItem v-for="(photo, index) in allPhotos" :key="index">
              <div class="p-1">
                <img
                  :src="photo || undefined"
                  :alt="'Additional photo ' + (index + 1)"
                  class="additional-photo w-full h-full object-cover rounded-lg"
                />
              </div>
            </CarouselItem>
          </CarouselContent>
          <CarouselPrevious />
          <CarouselNext />
        </Carousel>
        <Carousel
          class="relative w-full max-w-xs"
          @init-api="(val) => (emblaThumbnailApi = val)"
        >
          <CarouselContent class="flex gap-1 ml-0">
            <CarouselItem
              v-for="(photo, index) in allPhotos"
              :key="index"
              class="pl-0 basis-1/4 cursor-pointer"
              @click="onThumbClick(index)"
            >
              <div
                class="p-1"
                :class="index === selectedIndex ? '' : 'opacity-50'"
              >
                <img
                  :src="photo || undefined"
                  :alt="'Additional photo ' + (index + 1)"
                  class="additional-photo w-full h-full object-cover rounded-lg"
                />
              </div>
            </CarouselItem>
          </CarouselContent>
        </Carousel>
      </div>
      <div class="relative">
        <h1 class="text-3xl font-semibold mb-4">{{ product.name }}</h1>
        <p class="text-gray-700 mb-4">{{ product.description }}</p>
        <p class="text-gray-500 font-bold mb-4">
          {{ t('price') }}: {{ product.price }} eur
        </p>
        <span class="flex items-center mb-4">
          <p class="font-medium text-base mr-2">
            {{ t('stock') }}: {{ tweenedStockAmount.value.toFixed(0) }}
          </p>
          <img src="@/assets/live-dot.gif" width="20px"/>
          <p class="font-bold text-sm">LIVE</p>
        </span>
        <Button
          :disabled="isOutOfStock(product.stock_quantity)"
          class="absolute right-0"
        >
          {{ t('addToCart') }}
        </Button>
        <div
          class="brand-info flex items-center mb-6 absolute bottom-0 left-0 w-full p-4 bg-white"
        >
          <div
            class="brand-photo-container w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mr-4"
          >
            <img
              v-if="product?.brand?.photo"
              :src="product.brand.photo"
              alt="Brand photo"
              class="brand-photo w-full h-full object-cover rounded-full"
            />
            <span v-else class="text-gray-500">No Image</span>
          </div>
          <div>
            <p class="text-gray-900 font-semibold">{{ product.brand?.name }}</p>
            <p class="text-gray-700">{{ product.brand?.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import {
  Carousel,
  type CarouselApi,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '@/components/ui/carousel'
import { useFetchQuery } from '@/composables/useQuery'
import { client } from '@/lib/client'
import { watchOnce } from '@vueuse/core'
import { defineProps, ref, watch, reactive, onBeforeUnmount } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import gsap from 'gsap'

const { t } = useI18n()

const emblaMainApi = ref<CarouselApi>()
const emblaThumbnailApi = ref<CarouselApi>()
const selectedIndex = ref(0)

function onSelect() {
  if (!emblaMainApi.value || !emblaThumbnailApi.value) return
  selectedIndex.value = emblaMainApi.value.selectedScrollSnap()
  emblaThumbnailApi.value.scrollTo(emblaMainApi.value.selectedScrollSnap())
}

function onThumbClick(index: number) {
  if (!emblaMainApi.value || !emblaThumbnailApi.value) return
  emblaMainApi.value.scrollTo(index)
}

watchOnce(emblaMainApi, (emblaMainApi) => {
  if (!emblaMainApi) return

  onSelect()
  emblaMainApi.on('select', onSelect)
  emblaMainApi.on('reInit', onSelect)
})

const route = useRoute('//products/[id]')

const { data: product } = useFetchQuery({
  watch: () => [route.params.id],
  load() {
    return client.GET(`/api/products/{product_id}`, {
      params: {
        path: {
          product_id: route.params.id,
        },
      },
    })
  },
  immediate: true,
})

function isOutOfStock(stock = 0) {
  return stock == 0
}

const selectedPhoto = ref(product.value?.photo || undefined)
const allPhotos = ref<string[]>([])
watch(product, (newProduct) => {
  selectedPhoto.value = newProduct?.photo || undefined
  allPhotos.value = [
    newProduct?.photo,
    ...(newProduct?.additional_photos || []),
  ].filter((photo): photo is string => !!photo)
})

const selectPhoto = (photo: any) => {
  if (!photo) return
  selectedPhoto.value = photo
}

const tweenedStockAmount = reactive({ value: 0 })

watch(product, (newProduct) => {
  gsap.to(tweenedStockAmount, {
    value: newProduct?.stock_quantity || 0,
    duration: 2,
  })
}, { deep: true })

const eventSource = new EventSource(`${import.meta.env.VITE_API_URL}/api/products/${route.params.id}/stock`)

eventSource.onopen = () => {
    console.log('EventSource connected')
}

eventSource.addEventListener('stockUpdate', function (event) {
  if (product.value) {
    const newQuantity = parseInt(event.data)
    product.value.stock_quantity = newQuantity
  }
});

eventSource.onerror = (error) => {
    console.error('EventSource failed', error)
    eventSource.close()
}

onBeforeUnmount(() => {
  eventSource.close()
  console.log("Closed event source")
})

</script>
