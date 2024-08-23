<script setup lang="ts">
import { defineComponent, onMounted, ref, watch, type Ref } from 'vue';
import { reservationApi, shopApi } from '@/main';
import type { OpenRange, ReservedTimeRange, ShopWithOpenRange } from '@/api/types';
import DayTimeline from './DayTimeline.vue';
import { useI18n } from 'vue-i18n';
import { getDateOfWeekDay, minutesToTime, reformatTime, timeToMinutes } from '../utils';
import { type Task } from '../types';
import { useToast } from 'primevue/usetoast';
import EditReservationDialog from './dialog/EditReservationDialog.vue';
import AddReservationDialog from './dialog/AddReservationDialog.vue';


const toast = useToast();

const $t = useI18n().t;

const props = defineProps({
    shopId: { type: Number, required: true },
    year: { type: Number, required: true },
    weekNumber: { type: Number, required: true }
}); reformatTime

const displayedTasks: Ref<Task[][]> = ref([[], [], [], [], [], [], []] as Task[][]);
const dayBounds = ref({ start_time: timeToMinutes('12:00'), end_time: timeToMinutes('13:00') })
const shopData: Ref<ShopWithOpenRange | null> = ref(null);

const editTask: Ref<Task | null> = ref(null);
const editVisible = ref(false);
const addVisible = ref(false);
const dialogTimeStart: Ref<Date> = ref(new Date());
const dialogTimeEnd: Ref<Date> = ref(new Date());
const dialogSelectedDay: Ref<number> = ref(0);

const isLoading = defineModel("loading", {
    type: Boolean,
    default: false
});

// Watch the props 
watch(
    () => props.weekNumber + props.year * 53,
    () => {
        fetchShop(props.shopId);
    }
);


function colorTask(task: ReservedTimeRange) {

    if (task.status === -1) return '#ff9142';
    if (task.status === -2) return '#42ff4c';
    if (task.status > 0) return '#42f2ff';
    return '#9e9e9e';
}


function onLoadShop(shop: ShopWithOpenRange) {
    shopData.value = shop;
    dayBounds.value = shop.open_ranges.reduce(
        (acc: { start_time: number, end_time: number }, range: OpenRange) => {
            if (timeToMinutes(range.start_time) < acc.start_time) acc.start_time = timeToMinutes(range.start_time);
            if (timeToMinutes(range.end_time) > acc.end_time) acc.end_time = timeToMinutes(range.end_time) + 30;
            return acc;
        },
        { start_time: timeToMinutes('12:00'), end_time: timeToMinutes('13:00') }
    );



    reservationApi.getPlanning(shop.id, props.year, props.weekNumber).then(
        planning => {

            displayedTasks.value = planning.map(
                (day_planning, index) => {

                    const result: Task[] = shop.open_ranges.filter(
                        (range: OpenRange) => index === range.day
                    ).map(
                        (range: OpenRange) => ({
                            start_time: timeToMinutes(range.start_time),
                            end_time: timeToMinutes(range.end_time),
                            color: 'gray',
                            title: $t('message.shop_open'),
                            description: `${reformatTime(range.start_time)} - ${reformatTime(range.end_time)}`,
                            id: null,
                            _row: undefined,
                            cursor: 'arrow',
                        })
                    );

                    result.push(...day_planning.map(
                        (range: ReservedTimeRange) => ({
                            start_time: timeToMinutes(range.start_time),
                            end_time: timeToMinutes(range.start_time) + range.duration_minutes,
                            color: colorTask(range),
                            title: (range.status < 0) ? $t(range.title) : range.title,
                            description: `${reformatTime(range.start_time)} - ${minutesToTime(timeToMinutes(range.start_time) + range.duration_minutes)}`,
                            id: range.id,
                            _row: undefined,
                            cursor: (range.status != -1) ? 'pointer' : 'arrow',
                        })
                    ));

                    return result;
                }
            )
            isLoading.value = false;
        }
    ).catch(
        (error) => {
            if (error.response?.data) {
                toast.add({ severity: 'error', summary: $t('error.title'), detail: $t(error.response?.data.detail, { min_time: shopData.value?.min_time, max_time: shopData.value?.max_time }) });
            } else {
                toast.add({ severity: 'error', summary: $t('error.title'), detail: $t('error.reservation.unknown') });
            }
        }
    );
}


async function fetchShop(shopId: number) {
    isLoading.value = true;
    shopApi.get(shopId).then(
        (shop) => {
            onLoadShop(shop);
        },
        error => {
            console.error(error)
        }
    );
}

onMounted(
    () => {
        fetchShop(props.shopId);
    }
)




function onTaskClick(day: number, task: Task) {
    addVisible.value = false;
    if (task.id !== null) {
        if (task.cursor === 'pointer') {
            editTask.value = task;
            // Get the corresponding date
            const task_date = getDateOfWeekDay(props.year, props.weekNumber, day);
            const task_date_ms = task_date.getTime();
            // Set the date to the task start time
            dialogTimeStart.value = new Date(task_date_ms + (task.start_time) * 60 * 1000);
            // Set the end time on the same day
            dialogTimeEnd.value = new Date(task_date_ms + (task.end_time) * 60 * 1000);
            dialogSelectedDay.value = day;
            editVisible.value = true;
        }
    }
}


function onAddTask(day: number) {
    editVisible.value = false;
    addVisible.value = true;
    dialogSelectedDay.value = day;

    // Get the corresponding date
    const task_date = getDateOfWeekDay(props.year, props.weekNumber, day);
    const task_date_ms = task_date.getTime();

    // Get the first 1-hour slot inside an open range with less than shop.volunteers reservations
    const open_ranges = shopData.value?.open_ranges.filter(
        (range: OpenRange) => range.day === day
    );


    const volunteers = shopData.value?.volunteers;

    if (!open_ranges?.length) {
        console.error("No open range found");
        return;
    }

    if (!volunteers) {
        console.error("shop.volunteers is null");
        return;
    }
    dialogTimeStart.value = new Date(task_date_ms + timeToMinutes(open_ranges[0].start_time) * 60 * 1000);
    dialogTimeEnd.value = new Date(dialogTimeStart.value.getTime() + shopData.value?.min_time! * 60 * 1000);

    for (const open_range of open_ranges)
        for (let start_time = timeToMinutes(open_range.start_time); start_time < timeToMinutes(open_range.end_time); start_time += shopData.value?.min_time!) {
            const end_time = start_time + shopData.value?.min_time!;
            const reservations = displayedTasks.value[day].filter(
                (task: Task) => task.start_time < end_time && task.end_time > start_time
            ).length;

            if (reservations < volunteers) {
                dialogTimeStart.value = new Date(task_date_ms + start_time * 60 * 1000);
                dialogTimeEnd.value = new Date(task_date_ms + end_time * 60 * 1000);
                return;

            }
        }


}






</script>
<template>
    <div v-if="shopData">
        <div class="weekview">
            <DayTimeline v-for="[index, tasks] in displayedTasks.entries()" :key="index" :title="$t(`day.${index}`)" :tasks="tasks"
                :startOfDay="dayBounds.start_time" :endOfDay="dayBounds.end_time" @click-task="(task: Task) => onTaskClick(index, task)"
                @add-task="onAddTask(index)" />
        </div>
    </div>
    <EditReservationDialog :date="getDateOfWeekDay(props.year, props.weekNumber, dialogSelectedDay)" :task="editTask" v-model:visible="editVisible"
        :shopData="shopData" @update:task="fetchShop(props.shopId)" v-model:start-date="dialogTimeStart" v-model:end-date="dialogTimeEnd"
        v-if="editTask" />
    <AddReservationDialog @update:tasks="fetchShop(props.shopId)" v-model:visible="addVisible" :shopData="shopData"
        v-model:start-date="dialogTimeStart" v-model:end-date="dialogTimeEnd" v-if="addVisible" />
</template>

<script lang="ts">
export default defineComponent({
    name: 'WeekViewer',
    components: {
        DayTimeline,
        EditReservationDialog,
        AddReservationDialog
    },
});
</script>

<style scoped>
.weekview {
    display: flex;
    gap: 0 rem;
    width: 100%;
    justify-content: space-around;
}
</style>
