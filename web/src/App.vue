<script setup lang="ts">
import { RouterView } from 'vue-router'

import { defineComponent } from 'vue'
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';

</script>

<script lang="ts">
export default defineComponent({
  name: 'App',
  components: {
    RouterView,
    Toast,
    ConfirmDialog
  }
})
</script>

<template>
  <Toast />

  <RouterView />
  <ConfirmDialog style="white-space: pre-line"></ConfirmDialog>
</template>

<style></style>
