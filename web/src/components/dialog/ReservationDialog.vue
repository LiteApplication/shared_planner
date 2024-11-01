<template>
    <Dialog modal v-model:visible="visibleModel" :header="title" id="reservation-dialog">
        <p class="text-surface-500 dark:text-surface-400 block mb-8">{{ description }}</p>
        <div class="flex flex-col gap-2 mb-8">
            <IftaLabel v-if="showUsers">
                <Select v-model="selectedUserModel" :options="users" option-label="full_name" fluid input-id="user"
                    :empty-message="$t('admin.reservations.no_user_selected')" />
                <label for="user">{{ $t('message.reservation.user') }}</label>
            </IftaLabel>
            <IftaLabel v-if="showDate">
                <DatePicker v-model="dateModel" fluid input-id="date" date-format="dd/mm/yy" class="w-full"
                    :invalid="!validateDates(shopData, startDate, endDate, setError, dayOfWeek, monday)" />
                <label for="date">{{ $t('message.reservation.date') }}</label>
            </IftaLabel>
            <div class="flex flex-row gap-4 flex-wrap">
                <IftaLabel v-if="showTime" class="flex-grow">
                    <DatePicker v-model="startTimeModel" time-only fluid input-id="start_time" class="w-full"
                        :invalid="!validateDates(shopData, startDate, endDate, setError, dayOfWeek, monday)" :step-minute="30" />
                    <label for="start_time">{{ $t('message.reservation.start_time') }}</label>
                </IftaLabel>
                <IftaLabel v-if="showTime" class="flex-grow">
                    <DatePicker v-model="endTimeModel" time-only fluid input-id="end_time" class="w-full"
                        :invalid="!validateDates(shopData, startDate, endDate, setError, dayOfWeek, monday)" :step-minute="30" />
                    <label for="end_time">{{ $t('message.reservation.end_time') }}</label>
                </IftaLabel>
            </div>
            <IftaLabel v-if="showValidated">
                <Checkbox v-model="validatedModel" input-id="validated" />
                <label for="validated">{{ $t('message.reservation.validated') }}</label>
            </IftaLabel>
            <Message severity="error" v-if="errorMessage">{{ errorMessage }}</Message>
            <div class="flex gap-4 mt-1 flex-wrap">
                <Button v-if="showDelete" class="w-full" @click="deleteClicked" severity="danger">{{ $t('message.reservation.delete') }}</Button>
                <div class="flex gap-4 w-full">
                    <Button class="w-1/2" @click="visibleModel = false" severity="secondary">{{ $t('message.cancel') }}</Button>
                    <Button class="w-1/2" @click="saveClicked" severity="primary">{{ $t('message.save') }}</Button>
                </div>
            </div>
        </div>
    </Dialog>
</template>

<script setup lang="ts">
import type { Shop, ShopWithOpenRange, User } from '@/api/types';
import { computed, ref, type PropType } from 'vue';
import { getMonday, getWeekDay, validateDates } from '@/utils';
import { defineComponent } from 'vue';
import Dialog from 'primevue/dialog';
import Button from 'primevue/button';
import Message from 'primevue/message';
import DatePicker from '../primevue/DatePicker';
import { useI18n } from 'vue-i18n';
import { useConfirm } from 'primevue/useconfirm';
import Select from 'primevue/select';
import Checkbox from 'primevue/checkbox';
import IftaLabel from 'primevue/iftalabel';

const $t = useI18n().t;
const confirm = useConfirm();


const startTimeModel = defineModel<Date>("startTime", {
    type: Date,
    default: new Date()
});
const endTimeModel = defineModel<Date>("endTime", {
    type: Date,
    default: new Date()
});
const dateModel = defineModel<Date>("date", {
    type: Date,
    default: new Date()
});
const selectedUserModel = defineModel<User | null>("selectedUser", {
    type: Object as PropType<User | null>,
    default: null
});
const validatedModel = defineModel<boolean>("validated", {
    type: Boolean,
    required: false,
});
const visibleModel = defineModel<boolean>("visible", {
    type: Boolean,
    default: false
});

const emit = defineEmits<
    {
        save: [startDate: Date, endDate: Date, user: User | null, validated: boolean];
        delete: [];
    }>();

const props = defineProps({
    showDate: {
        default: false,
        type: Boolean

    },
    showTime: {
        default: true,
        type: Boolean
    },
    showUsers: {
        default: false,
        type: Boolean
    },
    showValidated: {
        default: false,
        type: Boolean
    },
    showDelete: {
        default: false,
        type: Boolean
    },
    title: {
        required: true,
        type: String
    },
    description: {
        required: true,
        type: String
    },
    users: {
        required: false,
        default: () => [],
        type: Array as PropType<User[]>
    },
    shopData: {
        required: false,
        default: null,
        type: Object as PropType<Shop | ShopWithOpenRange | null>
    }
})

const errorMessage = ref<string | null>(null);
const setError = (message: string | null) => {
    if (!message) {
        errorMessage.value = null;
        return;
    }
    errorMessage.value = $t(message, { min_time: props.shopData?.min_time, max_time: props.shopData?.max_time });
};
const startDate = computed(() => {
    const result = new Date(dateModel.value);
    result.setHours(startTimeModel.value.getHours());
    result.setMinutes(startTimeModel.value.getMinutes());
    return result;
});

const endDate = computed(() => {
    const result = new Date(dateModel.value);
    result.setHours(endTimeModel.value.getHours());
    result.setMinutes(endTimeModel.value.getMinutes());
    return result;
});


const dayOfWeek = computed(() => getWeekDay(dateModel.value));
const monday = computed(() => getMonday(dateModel.value));

function saveClicked() {
    if (!validateDates(props.shopData, startDate.value, endDate.value, setError, dayOfWeek.value, monday.value)) {
        emit('save', startDate.value, endDate.value, selectedUserModel.value?.id ? selectedUserModel.value : null, validatedModel.value ? true : false);
        return;
    }

    emit('save', startDate.value, endDate.value, selectedUserModel.value?.id ? selectedUserModel.value : null, validatedModel.value ? true : false);

    visibleModel.value = false;
}

function deleteClicked() {
    console.log("DElete clicked");
    confirm.require({
        header: $t('message.reservation.delete'),
        message: $t('message.reservation.confirm_delete'),
        acceptProps: { icon: 'pi pi-trash', label: $t('message.reservation.delete'), className: 'p-button-danger p-button' },
        rejectProps: { label: $t('message.cancel'), className: 'p-button-secondary p-button' },
        accept: () => {
            emit('delete');
            visibleModel.value = false;
        }
    });
}

</script>

<script lang="ts">
export default defineComponent({
    name: 'ReservationDialog',
    components: {
        // eslint-disable-next-line vue/no-reserved-component-names
        Dialog,
        IftaLabel,
        DatePicker,
        // eslint-disable-next-line vue/no-reserved-component-names
        Button,
        // eslint-disable-next-line vue/no-reserved-component-names
        Select,
        Checkbox,
        Message
    },
});

</script>

<style lang="scss" scoped>
#reservation-dialog {
    width: 100%;
    max-width: 500px;
    padding: 0;
    margin: 0;
}
</style>
