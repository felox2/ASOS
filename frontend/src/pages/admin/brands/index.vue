<template>
    <AdminNavBar />
    <div class="flex items-center justify-center ">
        <Card class="mx-10 mt-2 w-full">
            <CardHeader>
                <CardTitle>{{ t('Brands') }}</CardTitle>
            </CardHeader>
            <CardContent >
                <ManagementTable
                    v-if="brands"
                    :headers="headers"
                    :data="brands"
                    :onAction="deleteBrand"
                    :createAction="createBrand"
                    redirect="/admin/brands"
                    redirectKey="id"
                />
            </CardContent>
        </Card>

    </div>


    <BrandCreate v-model="isOpen" :created="reloadBrands"/>

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
import BrandCreate from '@/components/dialogs/BrandCreate.vue'
import AdminNavBar from '@/components/AdminNavBar.vue'


const { t } = useI18n()

const isOpen = ref(false)

const headers = [
    { title: 'Name', value: 'name' }
]

const { data: brands, reload: reloadBrands } = useFetchQuery({
	load() {
		return client.GET('/api/brands')
		},
		immediate: true,
})


function deleteBrand(row: any) {
    console.log('delete', row)
}

function createBrand() {
    isOpen.value = true
}

</script>