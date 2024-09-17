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
import handleError from '@/error_handler';


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
    const snapTo30 = (time: string) => {
        const minutes = timeToMinutes(time);
        return minutes - (minutes % 30);
    }
    dayBounds.value = shop.open_ranges.reduce(
        (acc: { start_time: number, end_time: number }, range: OpenRange) => {
            if (snapTo30(range.start_time) < acc.start_time) acc.start_time = snapTo30(range.start_time);
            if (snapTo30(range.end_time) > acc.end_time) acc.end_time = snapTo30(range.end_time) + 30;
            return acc;
        },
        { start_time: timeToMinutes('12:00'), end_time: timeToMinutes('13:00') }
    );


    const weekStart = getDateOfWeekDay(props.year, props.weekNumber, 0).getTime();
    const shopStart = (new Date(shop.available_from)).getTime();
    const shopEnd = (new Date(shop.available_until)).getTime();

    const days = (n: number) => 1000 * 60 * 60 * 24 * n;
    reservationApi.getPlanning(shop.id, props.year, props.weekNumber).then(
        planning => {

            displayedTasks.value = planning.map(
                (day_planning, index) => {

                    const result: Task[] = shop.open_ranges.filter(
                        (range: OpenRange) => (index === range.day) && (weekStart + days(index) >= shopStart) && (weekStart + days(index) <= shopEnd)
                    ).map(
                        (range: OpenRange) => ({
                            start_time: timeToMinutes(range.start_time),
                            end_time: timeToMinutes(range.end_time),
                            color: 'gray',
                            title: $t('message.shops.open'),
                            description: `${reformatTime(range.start_time)} - ${reformatTime(range.end_time)}`,
                            id: null,
                            _row: undefined,
                            cursor: 'arrow',
                            status: -3
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
                            status: range.status
                        })
                    ));

                    return result;
                }
            )
            isLoading.value = false;
        }
    ).catch(
        handleError(toast, $t, "error.shop.not_loaded")
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
    const min_time = shopData.value?.min_time || 60;

    dialogTimeStart.value = new Date(task_date_ms + 10 * 60 * 60 * 1000); // 10:00
    dialogTimeEnd.value = new Date(dialogTimeStart.value.getTime() + min_time * 60 * 1000);

    if (!open_ranges?.length) {
        console.error("No open range found");
        return;
    }

    if (!volunteers) {
        console.error("shop.volunteers is null");
        return;
    }
    dialogTimeStart.value = new Date(task_date_ms + timeToMinutes(open_ranges[0].start_time) * 60 * 1000);
    dialogTimeEnd.value = new Date(dialogTimeStart.value.getTime() + min_time * 60 * 1000);

    for (const open_range of open_ranges)
        for (let start_time = timeToMinutes(open_range.start_time); start_time < timeToMinutes(open_range.end_time); start_time += min_time) {
            const end_time = start_time + min_time * 2;
            const reservations = displayedTasks.value[day].filter(
                (task: Task) => task.start_time < end_time && task.end_time > start_time && task.status !== -3
            );

            if (reservations.length < volunteers && !reservations.some((task: Task) => { return task.status === -2 })) {
                dialogTimeStart.value = new Date(task_date_ms + start_time * 60 * 1000);
                dialogTimeEnd.value = new Date(task_date_ms + end_time * 60 * 1000);
                return;

            }
        }


}






</script>
<template>
    <div v-if="shopData">
        <div id="legende" class="rounded p-4 m-2 mb-0 bg-slate-100 dark:bg-slate-800">
            <div class="flex">
                <div id="open" class="rounded square-legend"></div>
                <p>{{ $t("message.shops.open") }}</p>
            </div>
            <div class="flex">
                <div id="booked" class="rounded square-legend"></div>
                <p>{{ $t("message.reservation.booked") }}</p>
            </div>
            <div class="flex">
                <div id="booked-by-you" class="rounded square-legend"></div>
                <p>{{ $t("message.reservation.booked_by_you") }}</p>
            </div>


        </div>
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

.square-legend {
    width: 20px;
    height: 20px;
    border: 1px solid black;
    display: inline-block;
    margin-right: 5px;
}

#open {
    background-color: gray;
}

#booked {
    background-color: #ff9142;
}

#booked-by-you {
    background-color: #42ff4c;
}
</style>
