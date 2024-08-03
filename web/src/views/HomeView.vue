<script setup lang="ts">

import { defineComponent, onMounted, ref } from 'vue'
import LoadingScreen from '@/components/LoadingScreen.vue';
import { useRouter } from 'vue-router';

import { authApi } from '@/main';
import WeekViewer from '@/components/WeekViewer.vue';
import DayTimeline from '@/components/DayTimeline.vue';
import { timeToMinutes } from '../utils';
import type { Task } from '../types';
const $router = useRouter();

let loading = ref(true);

async function fetchData() {
    authApi.me().then(
        (user) => {
            console.log("Logged in as", user);
            loading.value = false;
        },
        error => {
            if (error.response && error.response.status === 401) {
                $router.push('/login');
            } else {
                console.error(error);
            }
        }
    );
}

onMounted(() => {
    fetchData();
});




</script>
<template>
    <LoadingScreen :visible="loading" />
    <h1>{{ $t('message.hello_world') }}</h1>
    <p>
        <router-link to="/login">Login</router-link>
    </p>
    <DayTimeline title="Planning" :tasks="tasks" :startOfDay="timeToMinutes('08:00')" :endOfDay="timeToMinutes('14:00')" />
    <WeekViewer :shopId="1" :weekNumber="1" :year="2022" />

</template>

<script lang="ts">
export default defineComponent({
    name: 'HomeView',
    components: {
        LoadingScreen,
        DayTimeline,
        WeekViewer,
    },
    data() {
        return {
            tasks: [
                { start_time: timeToMinutes('08:30'), end_time: timeToMinutes('09:30'), color: '#42A5F5', title: 'Task 1', description: 'This is a description', id: 0 },
                { start_time: timeToMinutes('09:00'), end_time: timeToMinutes('10:00'), color: '#66BB6A', title: 'Task 2', description: 'This is a description', id: 1 },
                { start_time: timeToMinutes('11:00'), end_time: timeToMinutes('12:00'), color: '#FFA726', title: 'Task 3', description: 'This is a description', id: 2 },
                { start_time: timeToMinutes('11:30'), end_time: timeToMinutes('12:30'), color: '#AB47BC', title: 'Task 4', description: 'This is a description', id: 3 },
                { start_time: timeToMinutes('11:45'), end_time: timeToMinutes('12:35'), color: '#0505f5', title: 'Task 5', description: 'This is a description', id: 4 },
                { start_time: timeToMinutes('12:00'), end_time: timeToMinutes('13:30'), color: '#05f505', title: 'Task 6', description: 'This is a description', id: 5 }
            ] as Task[]
        };
    }



})
</script>
<style></style>