<script setup lang="ts">
import { computed, defineComponent, onMounted, ref, watch, type Ref } from 'vue';
import { reservationApi, shopApi } from '@/main';
import type { OpenRange, ReservedTimeRange, ShopWithOpenRange, User } from '@/api/types';
import DayTimeline from './DayTimeline.vue';
import { useI18n } from 'vue-i18n';
import { getDateOfWeekDay, minutesToTime, networkDateTime, reformatTime, timeToMinutes } from '../utils';
import { type Task } from '../types';
import { useToast } from 'primevue/usetoast';
import ReservationDialog from './dialog/ReservationDialog.vue';
import handleError from '@/error_handler';


const toast = useToast();

const { t, d } = useI18n();

const props = defineProps({
    shopId: { type: Number, required: true },
    week: { type: String, required: true }, // Monday, yyyy-mm-dd
}); reformatTime

const displayedTasks: Ref<Task[][]> = ref([[], [], [], [], [], [], []] as Task[][]);
const dayBounds = ref({ start_time: timeToMinutes('12:00'), end_time: timeToMinutes('13:00') })
const shopData: Ref<ShopWithOpenRange | null> = ref(null);

const editTask: Ref<Task | null> = ref(null);
const editVisible = ref(false);
const addVisible = ref(false);
const dialogDate: Ref<Date> = ref(new Date());
const dialogTimeStart: Ref<Date> = ref(new Date());
const dialogTimeEnd: Ref<Date> = ref(new Date());
const dialogSelectedDay: Ref<number> = ref(0);

const isLoading = defineModel("loading", {
    type: Boolean,
    default: false
});

const titles = computed<string[]>(
    () => Array.from({ length: 7 }, (_, i) => d(new Date(props.week).setDate(new Date(props.week).getDate() + i), 'week'))
)

// Watch the props 
watch(
    () => props.week,
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


    const weekStart = (new Date(props.week)).getTime();
    const shopStart = (new Date(shop.available_from)).getTime();
    const shopEnd = (new Date(shop.available_until)).getTime();

    const days = (n: number) => 1000 * 60 * 60 * 24 * n;
    reservationApi.getPlanning(shop.id, props.week).then(
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
                            title: t('message.shops.open'),
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
                            title: (range.status < 0) ? t(range.title) : range.title,
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
        handleError(toast, t, "error.shop.not_loaded")
    );
}


async function fetchShop(shopId: number) {
    isLoading.value = true;
    shopApi.get(shopId).then(
        (shop) => {
            onLoadShop(shop);
        }
    ).catch(
        handleError(toast, t, "error.shop.unknown")
    );
}

onMounted(
    () => {
        fetchShop(props.shopId);
    }
)




function onTaskClick(day: number, task: Task) {
    console.log(task);
    addVisible.value = false;
    if (task.id !== null) {
        if (task.cursor === 'pointer') {
            editTask.value = task;
            // Get the corresponding date
            const task_date = getDateOfWeekDay(props.week, day);
            const task_date_ms = task_date.getTime();
            const tz_offset = task_date.getTimezoneOffset() * 60 * 1000;
            // Set the date to the task start time
            dialogTimeStart.value = new Date(task_date_ms + (task.start_time) * 60 * 1000 + tz_offset);
            // Set the end time on the same day
            dialogTimeEnd.value = new Date(task_date_ms + (task.end_time) * 60 * 1000 + tz_offset);
            dialogDate.value = task_date;
            dialogSelectedDay.value = day;
            editVisible.value = true;
        }
    }
}

function addTaskTime(day: number, { time }: { time: string }) {
    dialogDate.value = getDateOfWeekDay(props.week, day);
    const task_date_ms = dialogDate.value.getTime();
    dialogTimeStart.value = new Date(task_date_ms + timeToMinutes(time) * 60 * 1000);
    // Add the timezone offset
    dialogTimeStart.value.setMinutes(dialogTimeStart.value.getMinutes() + dialogTimeStart.value.getTimezoneOffset());
    if (shopData.value)
        dialogTimeEnd.value = new Date(dialogTimeStart.value.getTime() + shopData.value?.min_time * 60 * 2 * 1000);
    else dialogTimeEnd.value = new Date(dialogTimeStart.value.getTime() + 60 * 60 * 1000); // 1 hour by default

    dialogSelectedDay.value = day;
    editVisible.value = false;
    addVisible.value = true;

}


function onAddTask(day: number) {
    editVisible.value = false;
    addVisible.value = true;
    dialogSelectedDay.value = day;

    // Get the corresponding date
    dialogDate.value = getDateOfWeekDay(props.week, day);
    const task_date_ms = dialogDate.value.getTime();

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


function addReservation(startDate: Date, endDate: Date, user: User | null, validated: boolean) {
    if (!shopData.value) {
        console.error("shopData is null");
        return;
    }
    reservationApi.reserve(shopData.value.id,
        { duration_minutes: (endDate.getTime() - startDate.getTime()) / 1000 / 60, start_time: networkDateTime(startDate) }
    ).then(
        () => {
            fetchShop(props.shopId);
            addVisible.value = false;
        }
    ).catch(
        handleError(toast, t, "error.reservation.not_added")
    );

}

function updateReservation(startDate: Date, endDate: Date) {
    if (!editTask.value) {
        console.error("editTask is null");
        return;
    }
    reservationApi.update(editTask.value.id!,
        { duration_minutes: (endDate.getTime() - startDate.getTime()) / 1000 / 60, start_time: networkDateTime(startDate) }
    ).then(
        () => {
            fetchShop(props.shopId);
            editVisible.value = false;
        }
    ).catch(
        handleError(toast, t, "error.reservation.not_updated")
    );
}

function deleteReservation() {
    if (!editTask.value) {
        console.error("editTask is null");
        return;
    }
    reservationApi.cancel(editTask.value.id!).then(
        () => {
            fetchShop(props.shopId);
            editVisible.value = false;
        }
    ).catch(
        handleError(toast, t, "error.reservation.not_deleted")
    );
}





</script>
<template>
    <div v-if="shopData">
        <div id="legend" class="rounded p-4 m-4 mb-0 bg-slate-100 dark:bg-slate-800">
            <div class="flex">
                <div id="open" class="rounded square-legend"></div>
                <p>{{ t("message.shops.open") }}</p>
            </div>
            <div class="flex">
                <div id="booked" class="rounded square-legend"></div>
                <p>{{ t("message.reservation.booked") }}</p>
            </div>
            <div class="flex">
                <div id="booked-by-you" class="rounded square-legend"></div>
                <p>{{ t("message.reservation.booked_by_you") }}</p>
            </div>


        </div>
        <div class="weekview">
            <div class="weekview-container">

                <DayTimeline v-for="[index, tasks] in displayedTasks.entries()" :key="index" :title="titles[index]" :tasks="tasks"
                    :startOfDay="dayBounds.start_time" :endOfDay="dayBounds.end_time" @click-task="(task: Task) => onTaskClick(index, task)"
                    @add-task="onAddTask(index)" @time-clicked="time => addTaskTime(index, time)" />
            </div>
        </div>
    </div>
    <ReservationDialog :title="t('message.reservation.add_title')" :description="t('message.reservation.add_description')" show-date show-time
        :shop-data="shopData" v-model:visible="addVisible" v-model:date="dialogDate" v-model:start-time="dialogTimeStart"
        v-model:end-time="dialogTimeEnd" @save="addReservation"></ReservationDialog>
    <ReservationDialog :title="t('message.reservation.edit_title')" :description="t('message.reservation.edit_description')" show-time show-delete
        :shop-data="shopData" v-model:visible="editVisible" v-model:date="dialogDate" v-model:start-time="dialogTimeStart"
        v-model:end-time="dialogTimeEnd" @save="updateReservation" @delete="deleteReservation"></ReservationDialog>

</template>

<script lang="ts">
export default defineComponent({
    name: 'WeekViewer',
    components: {
        DayTimeline,
        ReservationDialog,
    },
});
</script>

<style scoped>
.weekview {
    max-width: 100%;
    overflow-x: scroll;
}

.weekview-container {
    display: flex;
    gap: 0;
    flex-wrap: none;
    justify-content: space-evenly;
    min-width: fit-content;
    width: 100%;
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
