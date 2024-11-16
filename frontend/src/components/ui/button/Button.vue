<script setup lang="ts">
import { cn } from '@/lib/utils'
import { Loader2 } from 'lucide-vue-next'
import { Primitive, type PrimitiveProps } from 'radix-vue'
import type { HTMLAttributes } from 'vue'
import { type ButtonVariants, buttonVariants } from '.'

interface Props extends PrimitiveProps {
  variant?: ButtonVariants['variant']
  size?: ButtonVariants['size']
  class?: HTMLAttributes['class']
  loading?: boolean
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  as: 'button',
})
</script>

<template>
  <Primitive
    :as="as"
    :as-child="asChild"
    :class="cn(buttonVariants({ variant, size }), props.class)"
    :disabled="disabled || loading"
  >
    <Loader2
      v-if="loading"
      :class="
        cn(
          'absolute animate-spin pointer-events-none opacity-0',
          loading && 'opacity-100'
        )
      "
    />

    <div :class="cn(loading && 'opacity-0')">
      <slot />
    </div>
  </Primitive>
</template>
