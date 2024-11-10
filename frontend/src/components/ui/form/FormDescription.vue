<script lang="ts" setup>
import { cn } from '@/lib/utils'
import type { HTMLAttributes } from 'vue'
import { useFormField } from './useFormField'

const props = defineProps<{
  class?: HTMLAttributes['class']
}>()

const { formDescriptionId } = useFormField()
</script>

<template>
  <p :id="formDescriptionId" :class="cn('text-sm text-black/55', props.class)">
    <slot />
  </p>
</template>
