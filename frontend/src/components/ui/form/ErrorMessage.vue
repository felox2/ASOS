<script setup lang="ts">
import { cn } from '@/lib/utils'
import { CircleAlert } from 'lucide-vue-next'
import { ErrorMessage } from 'vee-validate'
import { HTMLAttributes, toValue } from 'vue'

interface Props {
  name: string
  class?: HTMLAttributes['class']
}

const props = defineProps<Props>()
</script>

<template>
  <ErrorMessage
    as="div"
    :name="toValue(name)"
    :class="cn('text-xs text-destructive flex items-center gap-1', props.class)"
    v-slot="{ message }"
    v-bind="$attrs"
  >
    <CircleAlert class="size-3 mt-[2px]" />
    <p>{{ message }}</p>
  </ErrorMessage>
</template>
