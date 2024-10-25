<script setup lang="ts">

import { computed, defineComponent, onMounted, ref, watch, type Ref } from 'vue'
import { useRouter } from 'vue-router';
import { useRouteParams } from '@vueuse/router';

import { useI18n } from 'vue-i18n';
import EnsureLoggedIn from '@/components/EnsureLoggedIn.vue';
import { exampleShopWithOpenRange, type ShopWithOpenRange } from '@/api/types';
import { shopApi } from '@/main';
import WeekViewer from '@/components/WeekViewer.vue';
import { DateToWeekNumber, getDateOfWeek, maxDate } from '@/utils';
import DatePicker from '@/components/primevue/DatePicker';
import handleError from '@/error_handler';
import { useToast } from 'primevue/usetoast';
import ShopHeader from '@/components/list/ShopHeader.vue';

const $router = useRouter();
const $t = useI18n().t;
const toast = useToast();

const shopId = useRouteParams("id", "0", { transform: Number });
const yearURL = useRouteParams("year", (new Date()).getFullYear(), { transform: Number });
const weekNumberURL = useRouteParams("week", DateToWeekNumber(new Date()), { transform: Number });

const isLoading = ref(true);

const datePicked = ref(getDateOfWeek(yearURL.value, weekNumberURL.value));
const shop: Ref<ShopWithOpenRange> = ref(exampleShopWithOpenRange);
const weekNumber = computed(() => DateToWeekNumber(datePicked.value));
const year = computed(() => datePicked.value.getFullYear());

onMounted(() => {
    shopApi.get(shopId.value).then(
        (r) => {
            shop.value = r;
            datePicked.value = maxDate(new Date(shop.value.available_from), datePicked.value);
        }
    ).catch(handleError(toast, $t, "error.shop.unknown")).finally(() => isLoading.value = false);
}
)

watch([shopId, weekNumber, year], () => {
    $router.push({ params: { id: shopId.value, year: year.value, week: weekNumber.value } });
}
)

</script>
<template>
    <EnsureLoggedIn :additional-loading="shop.id == -1 || isLoading" />
    <ShopHeader :shop="shop">
        <template #action>
            <DatePicker v-model="datePicked" showIcon fluid :date-format="$t('message.shops.week_format')" :showOnFocus="false"
                inputId="buttondisplay" :min-date="new Date(shop.available_from)" :max-date="new Date(shop.available_until)"
                :placeholder="$t('message.select_date')" show-week />
        </template>
    </ShopHeader>
    <WeekViewer :shop-id="shop.id" :year="year" :week-number="weekNumber" v-if="shop.id != -1" v-model:loading="isLoading" />
</template>

<script lang="ts">
export default defineComponent({
    name: 'ShopsView',
    components: {
        EnsureLoggedIn,
        DatePicker,
        WeekViewer,
        ShopHeader
    }
})
</script>
<style></style>
