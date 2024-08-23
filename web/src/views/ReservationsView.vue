<script setup lang="ts">

import { defineComponent, onMounted, ref, type Ref } from 'vue'
import { useRouter } from 'vue-router';

import { useToast } from 'primevue/usetoast';
import { useI18n } from 'vue-i18n';
import EnsureLoggedIn from '@/components/EnsureLoggedIn.vue';
import MainMenu from '@/components/MainMenu.vue';
import ReservationItem from '@/components/list/ReservationItem.vue';
import { exampleReservedTimeRange, type ReservedTimeRange } from '@/api/types';
import { reservationApi } from '@/main';

const $router = useRouter();
const toast = useToast();
const $t = useI18n().t;

const reservations: Ref<ReservedTimeRange[]> = ref([
    exampleReservedTimeRange,
    exampleReservedTimeRange,
    exampleReservedTimeRange,
    exampleReservedTimeRange,
]);


function updateReservations() {
    reservationApi.myReservations().then(
        (r) => { reservations.value = r }
    )
}

onMounted(() => {
    updateReservations();
}
)



</script>
<template>
    <EnsureLoggedIn />
    <MainMenu />
    <div>
        <ReservationItem v-for="(reservation, index) in reservations" :key="reservation.id === -1 ? index : reservation.id" :reservation="reservation"
            @update:reservation="updateReservations()" />
    </div>
</template>

<script lang="ts">
export default defineComponent({
    name: 'ReservationsView',
    components: {
        EnsureLoggedIn,
        MainMenu,
        ReservationItem
    }
})
</script>
<style></style>