<script setup>
import { RouterView } from 'vue-router'

import { defineComponent } from 'vue'

</script>

<script>
export default defineComponent({
  name: 'App',
  components: {
    RouterView
  }
})
</script>

<template>
  <RouterView />
</template>

<style></style>
