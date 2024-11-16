<script setup lang="ts">
import LogoutDialog from '@/components/dialogs/LogoutDialog.vue'
import ProductSearch from '@/components/ProductSearch.vue'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'
import { useDialog } from '@/composables/useDialog'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'
import { Search, ShoppingCart, UserRound, X } from 'lucide-vue-next'
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterLink, RouterView } from 'vue-router'

const { t, n } = useI18n()
const authStore = useAuthStore()
const cartStore = useCartStore()
const showLogoutDialog = useDialog(LogoutDialog)

const cartOpen = ref(false)
</script>

<template>
  <header
    class="sticky top-0 flex h-16 items-center gap-4 bg-background mx-auto px-6 md:px-20 max-w-7xl"
  >
    <nav
      class="hidden flex-col gap-6 text-lg font-medium md:flex md:flex-row md:items-center md:gap-5 md:text-sm lg:gap-6"
    >
      <RouterLink
        to="/"
        class="flex items-center gap-2 text-lg font-semibold md:text-base"
      >
        <span>EShop</span>
      </RouterLink>
    </nav>

    <div class="flex w-full items-center gap-4 md:ml-auto md:gap-2 lg:gap-4">
      <div class="mx-auto">
        <ProductSearch />
      </div>

      <div class="flex gap-2">
        <DropdownMenu v-if="authStore.user">
          <DropdownMenuTrigger as-child>
            <Button variant="secondary" size="icon" class="rounded-full">
              <UserRound class="h-5 w-5" />
              <span class="sr-only">Toggle user menu</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            <DropdownMenuLabel>My Account</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem :as="RouterLink" to="/settings">
              {{ t('settings') }}
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem @click="showLogoutDialog">
              {{ t('logout') }}
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>

        <Button
          v-else
          variant="secondary"
          size="icon"
          class="rounded-full"
          :as="RouterLink"
          to="/auth/login"
        >
          <UserRound class="h-5 w-5" />
          <span class="sr-only">Toggle user menu</span>
        </Button>

        <Popover v-model:open="cartOpen">
          <PopoverTrigger as-child>
            <Button
              variant="secondary"
              size="icon"
              class="rounded-full relative"
            >
              <ShoppingCart class="h-5 w-5" />

              <div
                v-if="cartStore.count"
                class="absolute top-0 right-0 -translate-y-1/4 translate-x-1/4 bg-primary text-xs text-white rounded-full w-4 h-4 flex items-center justify-center"
              >
                {{ cartStore.count }}
              </div>
            </Button>
          </PopoverTrigger>
          <PopoverContent class="w-96">
            <div>
              <div class="flex justify-between items-center mb-3">
                <h3 class="text-lg font-medium">{{ t('cart') }}</h3>

                <RouterLink to="/cart" @click="cartOpen = false">
                  {{ t('viewCart') }}
                </RouterLink>
              </div>
              <div class="flex flex-col gap-2">
                <div
                  v-for="item in cartStore.items"
                  class="flex gap-2 border-b pb-2"
                >
                  <img
                    v-if="item.product?.photo"
                    class="size-12 rounded aspect-square"
                    :src="item.product?.photo"
                  />

                  <div class="w-full">
                    <div class="flex justify-between w-full">
                      <h4>{{ item.product?.name }}</h4>
                      <Button
                        class="p-0 size-5"
                        variant="ghost"
                        @click="cartStore.removeCartItem(item)"
                      >
                        <X class="size-4" />
                      </Button>
                    </div>
                    <div class="flex justify-between items-center w-full">
                      <span class="text-sm text-muted-foreground">
                        {{ item.quantity }}x
                      </span>
                      <span>{{ n(item.product?.price || 0, 'currency') }}</span>
                    </div>
                  </div>
                </div>

                <div class="flex justify-between">
                  <span>{{ t('total') }}</span>
                  <span class="font-semibold">
                    {{ n(cartStore.total, 'currency') }}
                  </span>
                </div>
              </div>
            </div>
          </PopoverContent>
        </Popover>
      </div>
    </div>
  </header>

  <main class="p-4">
    <RouterView></RouterView>
  </main>
</template>
