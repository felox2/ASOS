<script setup lang="ts">
import {
  HoverCard,
  HoverCardContent,
  HoverCardTrigger,
} from '@/components/ui/hover-card'
import { HTMLAttributes } from 'vue'

defineProps<{
  contentClass?: HTMLAttributes['class']
}>()
</script>

<template>
  <HoverCard>
    <HoverCardTrigger as-child>
      <slot name="trigger"></slot>
    </HoverCardTrigger>
    <HoverCardContent :class="contentClass">
      <slot name="content"></slot>
    </HoverCardContent>
  </HoverCard>
</template>
