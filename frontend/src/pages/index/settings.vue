<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Separator } from '@/components/ui/separator'
import { cn } from '@/lib/utils'

interface Item {
  title: string
  href: string
}

const sidebarNavItems: Item[] = [
  {
    title: 'Profile',
    href: '/examples/forms',
  },
  {
    title: 'Account',
    href: '/examples/forms/account',
  },
  {
    title: 'Appearance',
    href: '/examples/forms/appearance',
  },
  {
    title: 'Notifications',
    href: '/examples/forms/notifications',
  },
  {
    title: 'Display',
    href: '/examples/forms/display',
  },
]
</script>

<template>
  <div class="max-w-7xl mx-auto md:px-20">
    <div class="space-y-0.5">
      <h2 class="text-2xl font-bold tracking-tight">Settings</h2>
      <p class="text-muted-foreground">
        Manage your account settings and set e-mail preferences.
      </p>
    </div>

    <Separator class="my-6" />

    <div class="flex flex-col space-y-8 lg:flex-row lg:space-x-12 lg:space-y-0">
      <aside class="-mx-4 lg:w-1/5">
        <nav class="flex space-x-2 lg:flex-col lg:space-x-0 lg:space-y-1">
          <Button
            v-for="item in sidebarNavItems"
            :key="item.title"
            as="a"
            :href="item.href"
            variant="ghost"
            :class="
              cn(
                'w-full text-left justify-start',
                $route.path === `${item.href}.html` && 'bg-muted hover:bg-muted'
              )
            "
          >
            {{ item.title }}
          </Button>
        </nav>
      </aside>
      <div class="flex-1 lg:max-w-2xl">
        <div class="space-y-6">
          <RouterView></RouterView>
        </div>
      </div>
    </div>
  </div>
</template>
