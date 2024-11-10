<template>
	<Dialog v-model:open="isOpen">
		<DialogContent>
			<DialogHeader>
				<DialogTitle>{{ t('createBrand')}}</DialogTitle>
				<DialogClose />
			</DialogHeader>
		
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
					<Button type="submit" class="btn btn-primary" >{{ t('save') }}</Button>
				</Form>
			
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

const form = ref({
	name: '',
	description: '',
	photo: null as File | null,
})

const emit = defineEmits(['created'])

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
	if (form.value.photo) {
		formData.append('photo', form.value.photo)
	}


   const reponse = await client.POST('/api/brands', {
		body: formData as any,
    }).catch((error) => {
        console.log(error)
    }).then(() => {
        emit('created')
        isOpen.value = false
    })
}

function required(value: any) {
	return value !== null && value !== undefined && value !== ''
}
</script>

