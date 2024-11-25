<template>
	<Dialog v-model:open="isOpen">
		<DialogOverlay />
		<DialogContent>
			<DialogHeader>
				<DialogTitle>Create Product</DialogTitle>
				<DialogClose />
			</DialogHeader>
			<DialogBody>
				<Form validate-on-input :submit="submitForm" class="space-y-2 mt-2">
					<FormField
						v-model="form.name"
						name="name"
						:rules="required"
						type="text"
						:label="t('name')"
						v-slot="{ componentField }"
						validate-on-blur
						validate-on-input
					>
						<FormItem>
							<FormControl>
								<Input
									v-bind="componentField"
									:placeholder="t('name')"
									:rules="required"
								/>
							</FormControl>
							<FormMessage />
						</FormItem>
					</FormField>

					<FormField
						v-model="form.description"
						name="description"
						:rules="required"
						:label="t('description')"
						v-slot="{ componentField }"
						validate-on-blur
						validate-on-input
					>
						<FormItem>
							<FormControl>
								<Input
									v-bind="componentField"
									:placeholder="t('description')"
									:rules="required"
								/>
							</FormControl>
							<FormMessage />
						</FormItem>
					</FormField>

					<FormField
						v-model="form.price"
						name="price"
						:rules="required"
						type="number"
						:label="t('price')"
						v-slot="{ componentField }"
						validate-on-blur
						validate-on-input
					>
						<FormItem>
							<FormControl>
								<Input
									v-bind="componentField"
									type="number"
									step="0.01"
									:placeholder="t('price')"
									:rules="required"
								/>
							</FormControl>
							<FormMessage />
						</FormItem>
					</FormField>

					<FormField
						v-model="form.stock_quantity"
						name="stock_quantity"
						:rules="required"
						type="number"
						:label="t('stock_quantity')"
						v-slot="{ componentField }"
						validate-on-blur
						validate-on-input
					>
						<FormItem>
							<FormControl>
								<Input
									v-bind="componentField"
									type="number"
									:placeholder="t('stock_quantity')"
									:rules="required"
								/>
							</FormControl>
							<FormMessage />
						</FormItem>
					</FormField>

					<FormField
						v-model="form.photo"
						name="photo"
						type="file"
						:label="t('photo')"
						v-slot="{ componentField }"
						validate-on-blur
						validate-on-input
					>
						<FormItem>
							<FormControl>
								<Input
									v-bind="componentField"
									type="file"
									@change="handleFileUpload"
									:placeholder="t('photo')"
									:rules="required"
								/>
							</FormControl>
							<FormMessage />
						</FormItem>
					</FormField>

					<FormField
						v-model="form.brand_id"
						name="brand_id"
						:rules="required"
						type="text"
						:label="t('brand')"
						v-slot="{ componentField }"
						validate-on-blur
						validate-on-input
					>
						<FormItem>
							<FormControl>
								<ComboBox
									v-if="brands"
									v-bind="componentField"
									:items="brands"
									:placeholder="t('brand')"
									label="name"
									value="id"
									:rules="required"
								/>
							</FormControl>
							<FormMessage />
						</FormItem>
					</FormField>

					<FormField
						v-model="form.category_ids"
						name="category_ids"
						:rules="required"
						type="text"
						:label="t('categories')"
						v-slot="{ componentField }"
						validate-on-blur
						validate-on-input
					>
						<FormItem>
							<FormControl>
								<ComboBox
									v-if="categories"
									v-bind="componentField"
									:items="categories"
									:placeholder="t('categories')"
									label="name"
									value="id"
									multiple
									:rules="required"
								/>
							</FormControl>
							<FormMessage />
						</FormItem>
					</FormField>

					<Button type="submit" class="btn btn-primary" >{{ t('save') }}</Button>
				</Form>
			</DialogBody>
		</DialogContent>
	</Dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { client } from '@/lib/client'
import { useRouter } from 'vue-router'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Select } from '@/components/ui/select'
import { Label } from '@/components/ui/label'
import { Button } from '@/components/ui/button'
import ComboBox from '@/components/ui/admin-combobox/Combobox.vue'
import {
	Form,
	FormControl,
	FormField,
	FormItem,
	FormMessage,
} from '@/components/ui/form'
import { useI18n } from 'vue-i18n'
import {
	Dialog,
	DialogContent,
	DialogHeader,
	DialogTitle,
	DialogClose,
} from '@/components/ui/dialog'
import { useFetchQuery } from '@/lib/useQuery'

const { t } = useI18n()
const router = useRouter()

const isOpen = defineModel<boolean>()

const emit = defineEmits(['created'])

const form = ref({
	name: '',
	description: '',
	price: 0,
	stock_quantity: 0,
	photo: null as File | null,
	brand_id: null,
	category_ids: []
})

const { data: brands, reload: reloadBrands } = useFetchQuery({
	load() {
		return client.GET('/api/brands')
		},
		immediate: true,
})


const { data: categories, reload: reloadCategories } = useFetchQuery({
	load() {
		return client.GET('/api/categories')
		},
		immediate: true,
})



const handleFileUpload = (event: Event) => {
	const target = event.target as HTMLInputElement
	if (target.files && target.files.length > 0) {
		form.value.photo = target.files[0]
	}
}

const submitForm = async () => {
	const formData = new FormData()
	formData.append('name', form.value.name)
	formData.append('description', form.value.description)
	formData.append('price', form.value.price.toString())
	formData.append('stock_quantity', form.value.stock_quantity.toString())
	if (form.value.photo) {
		formData.append('photo', form.value.photo)
	}
	if (form.value.brand_id) {
		formData.append('brand_id', form.value.brand_id)
	}
	form.value.category_ids.forEach((id: string) => {
		formData.append('category_ids', id)
	})

	await client.POST('/api/products', {
		body: formData as any,
	}).then(() => {
		isOpen.value = false
		emit('created')
	}).catch((error) => {
		console.error(error)
	})

	isOpen.value = false
}

function required(value: any) {
	return value !== null && value !== undefined && value !== ''
}
</script>

