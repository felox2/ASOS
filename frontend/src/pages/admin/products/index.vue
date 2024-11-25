<template>
	<AdminNavBar />
	<div class="flex items-center justify-center ">
		<Card class="mx-10 mt-2 w-full">
			<CardHeader>
				<CardTitle>{{ t('products') }}</CardTitle>
			</CardHeader>
			<CardContent >
				<ManagementTable
					v-if="products"
					:headers="headers"
					:data="products"
					:onAction="deleteProduct"
					:createAction="createProduct"
					redirect="/admin/products"
					redirectKey="id"


				/>
			</CardContent>
		</Card>

	</div>


	<ProductCreateFrom v-model="isOpen" />

</template>

<script setup lang="ts">
import ManagementTable from '@/components/ui/management-table/ManagementTable.vue'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { ref } from 'vue'
import ProductCreateFrom from '@/components/dialogs/ProductCreateFrom.vue'

import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { client } from '@/lib/client'
import { useFetchQuery } from '@/lib/useQuery'
import AdminNavBar from '@/components/AdminNavBar.vue'


const { t } = useI18n()

const isOpen = ref(false)

const headers = [
	{ title: 'Name', value: 'name' },
	{ title: 'Price', value: 'price' },
	{ title: 'Stock', value: 'stock_quantity' },
]

const { data: products, reload: reloadProducts } = useFetchQuery({
	load() {
		return client.GET('/api/products')
		},
		immediate: true,
})


function deleteProduct(row: any) {

    const confirmed = window.confirm("Are you sure you want to delete this product?");
    if (confirmed) {
        client.DELETE(`/api/products/{product_id}`, {
            params: { 
                path: {product_id: row.id} }
        }).then(() => {
            reloadProducts()
        })
        .catch(error => {
            console.error("Error deleting product:", error);
        });
    }
}

function createProduct() {
	isOpen.value = true
}

function createdNew(){
	isOpen.value = false
	reloadProducts()
}

</script>
