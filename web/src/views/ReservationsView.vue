<script setup lang="ts">

import { defineComponent, onMounted, ref, type Ref } from 'vue'
import { useRouter } from 'vue-router';

import { useToast } from 'primevue/usetoast';
import { useI18n } from 'vue-i18n';
import EnsureLoggedIn from '@/components/EnsureLoggedIn.vue';
import ReservationItem from '@/components/list/ReservationItem.vue';
import { exampleReservedTimeRange, type ReservedTimeRange } from '@/api/types';
import { reservationApi } from '@/main';
import Button from 'primevue/button';
import { PrimeIcons } from '@primevue/core/api';
import handleError from '@/error_handler';

const $router = useRouter();
const toast = useToast();
const $t = useI18n().t;

const reservations: Ref<ReservedTimeRange[]> = ref([
    exampleReservedTimeRange,
    exampleReservedTimeRange,
    exampleReservedTimeRange,
    exampleReservedTimeRange,
]);


function updateReservations(item: undefined | null | ReservedTimeRange = undefined, index: number | undefined = undefined) {
    // Optimistic update
    if (item != undefined && index != undefined) {
        if (item == null) {
            reservations.value.splice(index, 1);
        } else
            reservations.value[index] = item;
    }
    reservationApi.myReservations().then(
        (r) => { reservations.value = r } // Then we update the list with the real data
    ).catch(handleError(toast, $t, "error.reservation.unknown"));
}



onMounted(() => {
    updateReservations();
}
)



</script>
<template>
    <EnsureLoggedIn />
    <div v-if="reservations.length != 0">
        <ReservationItem v-for="(reservation, index) in reservations" :key="reservation.id === -1 ? index : reservation.id" :reservation="reservation"
            @update:reservation="updateReservations" />
    </div>
    <div v-else class="flex flex-col items-center">
        <h2 class="m-4 text-center text-xl">{{ $t("message.empty_list") }}</h2>
        <p>{{ $t("message.reservation.new_reservation_explanation") }}</p>
        <Button class="m-4" :label="$t('message.reservation.new_reservation_button')" @click="$router.push({ name: 'shops' })"
            :icon="PrimeIcons.PLUS" />
    </div>
</template>

<script lang="ts">
export default defineComponent({
    name: 'ReservationsView',
    components: {
        EnsureLoggedIn,
        ReservationItem,
        // eslint-disable-next-line vue/no-reserved-component-names
        Button
    }
})
</script>
<style></style>