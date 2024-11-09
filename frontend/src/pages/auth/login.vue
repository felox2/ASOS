<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Checkbox } from '@/components/ui/checkbox'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

const { t } = useI18n()
const authStore = useAuthStore()
const router = useRouter()
const loading = ref(false)
const form = ref({
  username: '',
  password: '',
  rememberMe: false,
})

definePage({
  meta: {
    guest: true,
  },
})

async function tryLogin() {
  try {
    loading.value = true

    await authStore.login(form.value)
    await router.replace('/')
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
        <CardTitle class="text-2xl">{{ t('login') }}</CardTitle>
      </CardHeader>
      <CardContent>
        <form @submit.prevent="tryLogin">
          <div>
            <Label for="username">{{ t('username') }}</Label>
            <Input
              v-model="form.username"
              id="username"
              autocomplete="username"
            />
          </div>

          <div class="mt-1">
            <Label for="password">{{ t('password') }}</Label>
            <Input
              v-model="form.password"
              id="password"
              type="password"
              autocomplete="current-password"
            />
          </div>

          <div class="flex justify-between items-center mt-3">
            <div class="flex items-center gap-x-2">
              <Checkbox id="remember_me" v-model:checked="form.rememberMe" />
              <Label for="remember_me">{{ t('rememberMe') }}</Label>
            </div>

            <Button :loading="loading">{{ t('signIn') }}</Button>
          </div>
        </form>
      </CardContent>
    </Card>
  </div>
</template>
