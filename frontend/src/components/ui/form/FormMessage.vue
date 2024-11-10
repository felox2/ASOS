<script lang="ts" setup>
import { CircleAlert } from 'lucide-vue-next'
import { ErrorMessage } from 'vee-validate'
import { toValue } from 'vue'
import { useFormField } from './useFormField'

const { name, formMessageId } = useFormField()
</script>

<template>
  <ErrorMessage
    :id="formMessageId"
    as="div"
    :name="toValue(name)"
    class="text-xs text-destructive flex items-center gap-1"
    v-slot="{ message }"
  >
    <CircleAlert class="size-3 mt-[2px]" />
    <p>{{ message }}</p>
  </ErrorMessage>
</template>
