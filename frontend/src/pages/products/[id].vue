<template>
	<Card class="container mx-auto p-4 mt-10" v-if="product">
	  <div class="product-detail max-w-4xl mx-auto shadow-md rounded-lg p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
		<div>
		  <div class="main-photo-container mb-6 h-96">
			<img :src="selectedPhoto" alt="Product photo" class="main-photo w-full h-full object-cover rounded-lg" />
		  </div>
		  <div class="additional-photos mb-6 flex overflow-x-auto space-x-4">
			<div
			  v-for="(photo, index) in allPhotos"
			  :key="index"
			  @click="selectPhoto(photo)"
			  class="additional-photo-container w-24 h-24 bg-gray-200 rounded-lg flex items-center justify-center cursor-pointer"
			>
			  <img :src="photo || undefined" :alt="'Additional photo ' + (index + 1)" class="additional-photo w-full h-full object-cover rounded-lg" />
			</div>
		  </div>
		</div>
		<div>
		  <h1 class="text-3xl font-semibold mb-4">{{ product.name }}</h1>
		  <p class="text-gray-700 mb-4">{{ product.description }}</p>
		  <p class="text-gray-500 font-bold mb-4">{{ t('price') }}: {{ product.price }} eur</p>
		  <p class="text-gray-700 mb-4">{{ t('stock') }} {{ product.stock_quantity }}</p>
		  <div class="brand-info flex items-center mb-6">
			<div class="brand-photo-container w-16 h-16 bg-gray-200 rounded-full flex items-center justify-center mr-4">
			  <img v-if="product?.brand?.photo" :src="product.brand.photo" alt="Brand photo" class="brand-photo w-full h-full object-cover rounded-full" />
			  <span v-else class="text-gray-500">No Image</span>
			</div>
			<div>
			  <p class="text-gray-900 font-semibold">{{ product.brand?.name }}</p>
			  <p class="text-gray-700">{{ product.brand?.description }}</p>
			</div>
		  </div>
		  
		  <div class="flex justify-end mt-10 mr-10" >
			<Button>{{ t('toCart') }}</Button>
		  </div>
		</div>
		
	</div>
</Card>
  </template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { defineProps } from 'vue';
import { useRoute } from 'vue-router';
import { useFetchQuery } from '@/composables/useQuery';
import { client } from '@/lib/client';
import { Card } from '@/components/ui/card';
import { useI18n } from 'vue-i18n';
import { Button } from '@/components/ui/button';

const { t } = useI18n();

const router = useRoute('/products/[id]')



const { data: product } = useFetchQuery({
	load() {
		const route = useRoute();
		return client.GET(`/api/products/{product_id}`,
			{
				params: {
					path:{
						product_id: router.params.id
					}
				}
			}
		);
	},
	immediate: true,
});

const selectedPhoto = ref(product.value?.photo || undefined);
const allPhotos = ref<string[]>([])
watch(product, (newProduct) => {
	selectedPhoto.value = newProduct?.photo || undefined;
	allPhotos.value = [newProduct?.photo, ...(newProduct?.additional_photos || [])].filter((photo): photo is string => !!photo);

});

const selectPhoto = (photo: any) => {
	if(!photo) return;
	selectedPhoto.value = photo;
};
</script>


