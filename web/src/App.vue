<script setup lang="ts">
import { RouterView } from 'vue-router'

import { defineComponent } from 'vue'

</script>

<script lang="ts">
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
