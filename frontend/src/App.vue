<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { Button } from './components/ui/button'
</script>

<template>
  <!-- <header>
    <div class="wrapper">
      <nav>
        <Button :as="RouterLink" to="/">Home</Button>
        <Button :as="RouterLink" to="/about">About</Button>
      </nav>
    </div>
  </header> -->

  <RouterView />
</template>
