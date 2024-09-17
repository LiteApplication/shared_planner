<template>
    <Dialog v-model:visible="addVisible" modal :header="$t('message.reservation.add_title')" :style="{ width: '25rem' }">
        <span class="text-surface-500 dark:text-surface-400 block mb-8">{{ $t('message.reservation.add_description') }}</span>
        <div class="flex flex-col gap-6 mb-8">
            <FloatLabel>
                <DatePicker v-model="dialogTimeStart" fluid input-id="start_time" showTime hourFormat="24" date-format="dd-mm-yy"
                    :invalid="!validateDates(shopData, dialogTimeStart, dialogTimeEnd, setError, dayOfWeek, week, year, $t)" />

                <label for="start_time">{{ $t('message.reservation.start_time') }}</label>
            </FloatLabel>
            <FloatLabel>
                <DatePicker v-model="dialogTimeEnd" time-only fluid input-id="end_time"
                    :invalid="!validateDates(shopData, dialogTimeStart, dialogTimeEnd, setError, dayOfWeek, week, year, $t)" />

                <label for="end_time">{{ $t('message.reservation.end_time') }}</label>
            </FloatLabel>
            <Message severity="error" v-if="errorMessage">{{ errorMessage }}</Message>
            <div class="flex gap-4 mt-1">
                <Button class="w-1/2" @click="addVisible = false" severity="secondary">{{ $t('message.cancel') }}</Button>
                <Button class="w-1/2" @click="onTaskAdded" severity="primary">{{ $t('message.save') }}</Button>
            </div>
        </div>
    </Dialog>

</template>

<script setup lang="ts">
import type { ShopWithOpenRange } from '@/api/types';
import { reservationApi } from '@/main';
import { DateToMinutes, DateToWeekNumber, getWeekDay, networkDateTime, validateDates } from '@/utils';
import { computed, ref, type PropType } from 'vue';
import { useI18n } from 'vue-i18n';
import { defineComponent } from 'vue';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import DatePicker from 'primevue/datepicker';
import Message from 'primevue/message';
import FloatLabel from 'primevue/floatlabel';
import { useToast } from 'primevue/usetoast';
import handleError from '@/error_handler';

const $t = useI18n().t;
const toast = useToast();

const errorMessage = ref<string | null>(null);

const setError = (message: string | null) => {
    errorMessage.value = message;
};

const emit = defineEmits(['update:tasks']);

const addVisible = defineModel<boolean>("visible",
    {
        type: Boolean,
        default: false,
    }
);

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

const props = defineProps({
    shopData: {
        type: Object as PropType<ShopWithOpenRange | null>,
        required: false
    }
});


const dayOfWeek = computed(() => getWeekDay(dialogTimeStart.value));
const week = computed(() => DateToWeekNumber(dialogTimeStart.value));
const year = computed(() => dialogTimeStart.value.getFullYear());

function onTaskAdded() {

    const task_date = new Date(dialogTimeStart.value.getTime());
    task_date.setHours(dialogTimeStart.value.getHours(), dialogTimeStart.value.getMinutes())
    const start_time = DateToMinutes(dialogTimeStart.value);
    const end_time = DateToMinutes(dialogTimeEnd.value);
    const duration_minutes = end_time - start_time;

    reservationApi.reserve(props.shopData!.id, {
        start_time: networkDateTime(task_date),
        duration_minutes: duration_minutes,
    }).then(
        () => {
            emit('update:tasks');
            addVisible.value = false;
        }
    ).catch(handleError(toast, $t, "error.reservation.unknown"));
}

</script>

<script lang="ts">
export default defineComponent({
    name: 'AddReservationDialog',
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
