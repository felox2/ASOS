<template>
    <AdminNavBar />
    <div class="flex items-center justify-center ">
        <Card class="mx-10 mt-2 w-full">
            <CardHeader>
                <CardTitle>{{ t('categories') }}</CardTitle>
            </CardHeader>
            <CardContent >
                <ManagementTable
                    v-if="categories"
                    :headers="headers"
                    :data="categories"
                    :onAction="deleteCategory"
                    :createAction="createCategory"
                    redirect="/admin/categories"
                />
            </CardContent>
        </Card>

    </div>


    <CategoryCreate v-model="isOpen" :created="reloadCategories"/>

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
import CategoryCreate from '@/components/dialogs/CategoryCreate.vue'
import AdminNavBar from '@/components/AdminNavBar.vue'


const { t } = useI18n()

const isOpen = ref(false)

const headers = [
    { title: 'Name', value: 'name' }
]

const { data: categories, reload: reloadCategories } = useFetchQuery({
	load() {
		return client.GET('/api/categories')
		},
		immediate: true,
})


function deleteCategory(row: any) {
    console.log('delete', row)
}

function createCategory() {
    isOpen.value = true
}

</script>