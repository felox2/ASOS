<template>
    <div class="max-w-6xl mx-auto">
        <Card>
        <CardHeader class="text-center">
            <CardTitle>{{ t('thanks') }}</CardTitle>
        </CardHeader>
        <CardContent class="text-center">
            {{ t('thanks_message') }}
        </CardContent>
        </Card>
    </div>

</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

const { t } = useI18n()



</script>