<script setup lang="ts">
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

const { t } = useI18n()
const authStore = useAuthStore()
const router = useRouter()

const open = defineModel<boolean>('open', { default: true })
const loading = ref(false)

async function logout() {
  try {
    loading.value = true

    await authStore.logout()

    router.push('/auth/login')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <Dialog v-model:open="open">
    <DialogContent class="sm:max-w-md">
      <DialogHeader>
        <DialogTitle>{{ t('dialog.logoutConfirmation.title') }}</DialogTitle>
        <DialogDescription>
          {{ t('dialog.logoutConfirmation.description') }}
        </DialogDescription>
      </DialogHeader>

      <DialogFooter>
        <DialogClose as-child>
          <Button variant="secondary" type="button">
            {{ t('no') }}
          </Button>
        </DialogClose>
        <Button variant="destructive" :loading="loading" @click="logout">
          {{ t('yes') }}
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>
