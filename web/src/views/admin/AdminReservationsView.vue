<script setup lang="ts">
import type { ReservedTimeRange, Shop, User } from '@/api/types';
import EnsureLoggedIn from '@/components/EnsureLoggedIn.vue';
import ReservationItem from '@/components/list/ReservationItem.vue';
import DatePicker from '@/components/primevue/DatePicker';
import { reservationApi, shopApi, usersApi } from '@/main';
import { getMonday } from '@/utils';
import Button from 'primevue/button';
import Select from 'primevue/select';
import Toolbar from 'primevue/toolbar';
import { defineComponent, onMounted } from 'vue';
import handleError from '@/error_handler';

import { ref } from "vue";
import { useI18n } from 'vue-i18n';
import { useToast } from 'primevue/usetoast';
import Skeleton from 'primevue/skeleton';

const $t = useI18n().t;
const toast = useToast();

const selectedUser = ref();
const loadedUsers = ref(false);
const users = ref<User[]>([]);

const datePicked = ref<null | Date>();

const selectedShop = ref();
const loadedShops = ref(false);
const shops = ref<Shop[]>([]);

const reservations = ref<ReservedTimeRange[]>([]);


onMounted(() => {
    usersApi.list().then((response) => {
        users.value = response;
        loadedUsers.value = true;
    }).catch(handleError(toast, $t, "error.user.unknown"));

    shopApi.list().then((response) => {
        shops.value = response;
        loadedShops.value = true;
    }).catch(handleError(toast, $t, "error.user.unknown"));
});

function search() {
    const shop_id = selectedShop.value ? selectedShop.value : undefined;
    const user_id = selectedUser.value ? selectedUser.value : undefined;
    const week = datePicked.value ? getMonday(datePicked.value) : undefined;

    reservationApi.search({ shop_id, user_id, monday: week }).then((response) => {
        reservations.value = response;
    }).catch(handleError(toast, $t, "error.reservation.unknown"));
}

</script>
<template>
    <EnsureLoggedIn require-admin />
    <Toolbar class="m-4">

        <template #start>
            <div class="card flex justify-center flex-wrap gap-4">
                <h1 class="m-2 text-center text-xl">{{ $t("admin.reservations.title") }}</h1>
                <Select v-model="selectedShop" :options="shops" filter optionLabel="name" optionValue="id" label
                    :placeholder="$t('admin.reservations.select_shop')" class="w-full md:w-56" :loading="!loadedUsers"
                    :empty-filter-message="$t('admin.reservations.filter_no_shop_found')" :filter-fields="['name', 'location']" show-clear />
                <Select v-model="selectedUser" :options="users" filter optionLabel="full_name" optionValue="id" label
                    :placeholder="$t('admin.reservations.select_user')" class="w-full md:w-56" :loading="!loadedUsers"
                    :empty-filter-message="$t('admin.reservations.filter_no_user_found')" :filter-fields="['full_name', 'group', 'email']"
                    show-clear />
                <DatePicker v-model="datePicked" showIcon fluid :date-format="$t('message.shops.week_format')" :showOnFocus="true"
                    inputId="buttondisplay" :placeholder="$t('message.select_date')" show-week showButtonBar class="w-full md:w-56" />
            </div>
        </template>
        <template #end>
            <Button label="Search" icon="pi pi-search" class="p-button-raised p-button-rounded p-button-success " @click="search" />
        </template>
    </Toolbar>


    <template v-if="reservations.length === 0">
        <div class="flex justify-center">
            <h1 class="m-4 text-center text-xl">{{ $t("admin.reservations.no_reservations") }}</h1>
        </div>
    </template>
    <ReservationItem v-for="reservation in reservations" :key="reservation.id" :reservation="reservation" @update:reservation="search()" show-users>
        <template #shopName="{ shop }">
            <h2 class="text-xl font-semibold align-middle" v-if="reservation.id != -1 && shop">{{ shop.name }}</h2>
            <Skeleton width="15rem" height="1.5rem" v-else></Skeleton>
            <span> - </span>
            <h3 v-if="reservation.title"> {{ reservation.status > 0 ? reservation.title : $t(reservation.title) }}</h3>

        </template>
    </ReservationItem>

</template>


<script lang="ts">
export default defineComponent({
    name: 'AdminReservationsView',
    components: {
        EnsureLoggedIn,
        Toolbar,
        // eslint-disable-next-line vue/no-reserved-component-names
        Select,
        DatePicker,
        // eslint-disable-next-line vue/no-reserved-component-names
        Button,
        ReservationItem,
        Skeleton
    }
});
</script>