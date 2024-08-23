<script setup lang="ts">
import { RouterView } from 'vue-router'

import { defineComponent } from 'vue'
import Toast from 'primevue/toast';

</script>

<script lang="ts">
export default defineComponent({
  name: 'App',
  components: {
    RouterView,
    Toast
  }
})
</script>

<template>
  <Toast />
  <RouterView />
</template>

<style></style>
