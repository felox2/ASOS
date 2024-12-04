<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { client } from '@/lib/client'
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

const { t } = useI18n()
const authStore = useAuthStore()
const router = useRouter()
const loading = ref(false)
const form = ref({
  email: '',
  name: '',
  password: '',
  password_repeat: '',
})

async function tryRegister() {
  try {
    loading.value = true

    // await authStore.login(form.value)
    await client.POST('/auth/register', {
      body: form.value,
    })
    await router.replace('/auth/login')
  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="h-screen flex items-center justify-center">
    <Card class="max-w-md w-full">
      <CardHeader>
        <CardTitle class="text-2xl">{{ t('register') }}</CardTitle>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="tryRegister">
          <div>
            <Label for="username">{{ t('username') }}</Label>
            <Input v-model="form.email" id="username" autocomplete="username" />
          </div>

          <div>
            <Label for="name">{{ t('name') }}</Label>
            <Input v-model="form.name" id="name" autocomplete="name" />
          </div>

          <div class="mt-1">
            <Label for="password">{{ t('password') }}</Label>
            <Input
              v-model="form.password"
              id="password"
              type="password"
              autocomplete="new-password"
            />
          </div>
          <div class="mt-1">
            <Label for="password_repeat">{{ t('password_repeat') }}</Label>
            <Input
              v-model="form.password_repeat"
              id="password_repeat"
              type="password"
              autocomplete="new-password"
            />
          </div>

          <div class="flex justify-end items-center mt-3">
            <Button :loading="loading">{{ t('register') }}</Button>
          </div>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
