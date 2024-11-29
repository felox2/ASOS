<template>
  <Dialog v-model:open="isOpen">
    <DialogContent>
      <DialogHeader>
        <DialogTitle>{{ t('createCategory') }}</DialogTitle>
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
          name="photo"
          type="file"
          :label="t('photo')"
          validate-on-blur
          validate-on-input
        >
          <FormItem>
            <FormControl>
              <Input
                type="file"
                @change="handleFileUpload"
                :placeholder="t('photo')"
                :rules="required"
              />
            </FormControl>
            <FormMessage />
          </FormItem>
        </FormField>
        <Button type="submit" class="btn btn-primary">{{ t('save') }}</Button>
      </Form>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { client } from '@/lib/client'
import { required } from '@/lib/rules'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

const { t } = useI18n()
const router = useRouter()

const isOpen = defineModel<boolean>()

const emit = defineEmits(['created'])

const form = ref({
  name: '',
  description: '',
  photo: null as File | null,
})

const handleFileUpload = (event: Event) => {
  var target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    form.value.photo = target.files[0]
    target.files = null
  }
}

const submitForm = async () => {
  var formData = new FormData()

  formData.append('name', form.value.name)
  formData.append('description', form.value.description)
  if (form.value.photo) {
    formData.append('photo', form.value.photo)
  }

  client
    .POST('/api/categories', {
      body: formData as any,
    })
    .then(() => {
      isOpen.value = false
      emit('created')
    })
    .catch((error) => {
      console.log(error)
    })
}
</script>
