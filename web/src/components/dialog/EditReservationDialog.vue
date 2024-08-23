<template>
    <Dialog v-model:visible="editVisible" modal :header="$t('message.reservation.edit_title')" :style="{ width: '25rem' }">
        <span class="text-surface-500 dark:text-surface-400 block mb-8">{{ $t('message.reservation.edit_description') }}</span>
        <div class="flex flex-col gap-6 mb-8">
            <FloatLabel>
                <DatePicker v-model="dialogTimeStart" time-only fluid input-id="start_time"
                    :invalid="!validateDates(shopData, dialogTimeStart, dialogTimeEnd, setError, dayOfWeek, $t)" />
                <label for="start_time">{{ $t('message.reservation.start_time') }}</label>
            </FloatLabel>
            <FloatLabel>
                <DatePicker v-model="dialogTimeEnd" time-only fluid input-id="end_time"
                    :invalid="!validateDates(shopData, dialogTimeStart, dialogTimeEnd, setError, dayOfWeek, $t)" />

                <label for="end_time">{{ $t('message.reservation.end_time') }}</label>
            </FloatLabel>
            <Message severity="error" v-if="errorMessage">{{ errorMessage }}</Message>
            <div class="flex gap-4 mt-1 flex-wrap">
                <Button class="w-full" @click="onTaskDelete" severity="danger">{{ $t('message.reservation.delete') }}</Button>
                <div class="flex gap-4 w-full">
                    <Button class="w-1/2" @click="editVisible = false" severity="secondary">{{ $t('message.cancel') }}</Button>
                    <Button class="w-1/2" @click="onTaskSave" severity="primary">{{ $t('message.save') }}</Button>
                </div>
            </div>
        </div>
        <div></div>


    </Dialog>
</template>

<script setup lang="ts">
import type { Shop, ShopWithOpenRange } from '@/api/types';
import { reservationApi } from '@/main';
import type { Task } from '@/types';
import { DateToMinutes, getWeekDay, networkDateTime, validateDates } from '@/utils';
import Button from 'primevue/button';
import DatePicker from 'primevue/datepicker';
import Dialog from 'primevue/dialog';
import FloatLabel from 'primevue/floatlabel';
import Message from 'primevue/message';
import { useToast } from 'primevue/usetoast';
import { computed, defineComponent, ref, type PropType } from 'vue';
import { useI18n } from 'vue-i18n';

const $t = useI18n().t;
const toast = useToast();

const editVisible = defineModel("visible",
    {
        type: Boolean,
        default: false,
    }
);
const props = defineProps({
    shopData: {
        type: Object as PropType<ShopWithOpenRange | Shop | null>,
        required: false
    },
    task: {
        type: Object as PropType<Task | null>,
        required: false
    }
})








const emit = defineEmits(["update:task"]);

const dialogTimeStart = defineModel<Date>("startDate",
    {
        type: Date,
        required: true
    }
);
const dialogTimeEnd = defineModel<Date>("endDate",
    {
        type: Date,
        required: true
    }
);
const errorMessage = ref<string | null>(null);

function setError(message: string | null) {
    errorMessage.value = message;
}


const dayOfWeek = computed(() => getWeekDay(dialogTimeStart.value));


function onTaskDelete() {

    if (!props.task) {
        console.error("task is null");
        return;
    }

    // Ask the user to confirm the deletion
    if (!confirm($t('message.reservation.confirm_delete'))) return

    reservationApi.cancel(props.task?.id!).then(() => {
        emit('update:task');
        editVisible.value = false;
    }).catch(
        (error) => {
            if (error.response?.data) {
                toast.add({
                    severity: 'error', summary: $t('error.title'), detail: $t(error.response?.data.detail, {
                        min_time: props.shopData?.min_time,
                        max_time: props.shopData?.max_time
                    })
                });
            } else {
                toast.add({ severity: 'error', summary: $t('error.title'), detail: $t('error.reservation.unknown') });
            }
        }
    );
}


function onTaskSave() {

    if (!props.task) {
        console.error("task is null");
        return;
    }

    const task_date = new Date(dialogTimeStart.value.getTime());
    task_date.setHours(dialogTimeStart.value.getHours(), dialogTimeStart.value.getMinutes())
    const start_time = DateToMinutes(dialogTimeStart.value);
    const end_time = DateToMinutes(dialogTimeEnd.value);
    const duration_minutes = end_time - start_time;

    reservationApi.update(props.task?.id!, {
        start_time: networkDateTime(task_date),
        duration_minutes: duration_minutes,
    }).then(
        () => {
            emit('update:task');
            editVisible.value = false;
        }
    ).catch(
        (error) => {
            if (error.response?.data) {
                toast.add({
                    severity: 'error', summary: $t('error.title'), detail: $t(error.response?.data.detail, {
                        min_time: props.shopData?.min_time,
                        max_time: props.shopData?.max_time
                    })
                });
            } else {
                toast.add({ severity: 'error', summary: $t('error.title'), detail: $t('error.reservation.unknown') });
            }
        }
    );

}

</script>

<script lang="ts">
export default defineComponent({
    name: 'EditReservationDialog',
    components: {
        // eslint-disable-next-line vue/no-reserved-component-names
        Dialog,
        FloatLabel,
        DatePicker,
        // eslint-disable-next-line vue/no-reserved-component-names
        Button,
        Message
    },
});

</script>