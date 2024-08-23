<template>
    <div class="bg-slate-200 dark:bg-slate-700 rounded-lg m-4 p-3">
        <div class="flex justify-between items-center">

            <div class="flex flex-col">
                <div class="flex flex-row gap-2 items-center">
                    <Button icon="pi pi-map-marker" severity="info" rounded outlined aria-label="Bookmark" as="a" :href="reservation.shop?.maps_link"
                        target="_blank" v-if="reservation.id != -1" />
                    <Skeleton shape="circle" size="2rem" class="mr-2" v-else></Skeleton>
                    <h2 class="text-xl font-semibold align-middle" v-if="reservation.id != -1">{{ reservation.shop?.name }}</h2>
                    <Skeleton width="15rem" height="1.5rem" v-else></Skeleton>
                </div>
                <p v-if="reservation.id != -1">
                    {{ $t('message.date') }} : <strong>
                        {{ date }}</strong>, {{ $t('message.time') }}: <strong>
                        {{ start }}</strong> - <strong>
                        {{ end }}</strong></p>
                <Skeleton class="mt-2" width="15rem" height="1rem" v-else></Skeleton>
            </div>
            <div class="flex flex-row gap-2">
                <Button icon="pi pi-pencil" aria-label="Edit" severity="warn" :disabled="reservation.validated" @click="editVisible = true"
                    v-if="reservation.id != -1" />
                <Skeleton shape="circle" size="2rem" v-else></Skeleton>
            </div>
        </div>
    </div>
    <EditReservationDialog :date="reservation.start_time" :task="editTask" v-model:visible="editVisible" :shopData="shop"
        v-model:start-date="dialogTimeStart" v-model:end-date="dialogTimeEnd" v-if="editVisible" @update:task="emit('update:reservation')" />
</template>

<script setup lang="ts">
import { type ShopWithOpenRange, type ReservedTimeRange, type Shop } from '@/api/types';
import { date_start_end, timeToMinutes } from '@/utils';
import Button from 'primevue/button';
import Skeleton from 'primevue/skeleton';
import { computed, defineComponent, onMounted, ref, type PropType } from 'vue';
import EditReservationDialog from '../dialog/EditReservationDialog.vue';
import type { Task } from '@/types';
import { shopApi } from '@/main';
import { useI18n } from 'vue-i18n';

const $t = useI18n().t;

const props = defineProps({
    reservation: {
        type: Object as PropType<ReservedTimeRange>,
        required: true
    }
});

const computed_date_start_end = computed(() => date_start_end(props.reservation.start_time, props.reservation.duration_minutes, $t("date_locale")));
const date = computed(() => computed_date_start_end.value.date);
const start = computed(() => computed_date_start_end.value.start);
const end = computed(() => computed_date_start_end.value.end);

const editVisible = ref(false);

const shop = ref<Shop | ShopWithOpenRange | null>(props.reservation.shop);
onMounted(() => {
    shopApi.get(props.reservation.shop!.id).then(result => shop.value = result);
});

const dialogTimeStart = ref(new Date(props.reservation.start_time));
const dialogTimeEnd = ref(new Date(dialogTimeStart.value.getTime() + props.reservation.duration_minutes * 60000));

const editTask = computed(() => {
    if (props.reservation.id === -1) return null;
    return {
        start_time: timeToMinutes(props.reservation.start_time),
        end_time: timeToMinutes(props.reservation.start_time) + props.reservation.duration_minutes,
        id: props.reservation.id,
        title: null,
        cursor: "pointer"
    } as Task;
});

const emit = defineEmits(['update:reservation']);

</script>

<script lang="ts">
export default defineComponent({
    name: 'ReservationItem',
    components: {
        // eslint-disable-next-line vue/no-reserved-component-names
        Button,
        Skeleton,
        EditReservationDialog
    }
})

</script>