<script setup lang="ts">

import { defineComponent } from 'vue'
import WeekViewer from '@/components/WeekViewer.vue';
import EnsureLoggedIn from '@/components/EnsureLoggedIn.vue';
import MainMenu from '@/components/MainMenu.vue';


</script>
<template>
    <EnsureLoggedIn />
    <MainMenu />

    <WeekViewer :shopId="1" :year="2024" :weekNumber="31" />
</template>

<script lang="ts">
export default defineComponent({
    name: 'HomeView',
    components: {
        EnsureLoggedIn,
        MainMenu,
        WeekViewer
    }
})
</script>
<style></style>