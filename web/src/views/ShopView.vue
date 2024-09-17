<script setup lang="ts">

import { computed, defineComponent, onMounted, ref, watch, type Ref } from 'vue'
import { useRouter } from 'vue-router';
import { useRouteParams } from '@vueuse/router';

import { useI18n } from 'vue-i18n';
import EnsureLoggedIn from '@/components/EnsureLoggedIn.vue';
import ShopItem from '@/components/list/ShopItem.vue';
import { exampleShopWithOpenRange, type ShopWithOpenRange } from '@/api/types';
import { shopApi } from '@/main';
import WeekViewer from '@/components/WeekViewer.vue';
import { DateToWeekNumber, maxDate } from '@/utils';
import DatePicker from '@/components/primevue/DatePicker';

const $router = useRouter();
const $t = useI18n().t;

const shopId = useRouteParams("id", "0", { transform: Number });

const isLoading = ref(true);

const datePicked = ref(new Date());
const shop: Ref<ShopWithOpenRange> = ref(exampleShopWithOpenRange);
const weekNumber = computed(() => DateToWeekNumber(datePicked.value));
const year = computed(() => datePicked.value.getFullYear());

onMounted(() => {
    shopApi.get(shopId).then(
        (r) => {
            shop.value = r;
            datePicked.value = maxDate(new Date(shop.value.available_from), new Date());
        }
    )
}
)

</script>
<template>
    <EnsureLoggedIn :additional-loading="shop.id == -1 || isLoading" />
    <ShopItem :shop="shop">
        <template #action>
            <DatePicker v-model="datePicked" showIcon fluid :date-format="$t('message.shops.week_format')" :showOnFocus="false"
                inputId="buttondisplay" :min-date="new Date(shop.available_from)" :max-date="new Date(shop.available_until)"
                :placeholder="$t('message.select_date')" :show-week="true" />
        </template>
    </ShopItem>
    <WeekViewer :shop-id="shop.id" :year="year" :week-number="weekNumber" v-if="shop.id != -1" v-model:loading="isLoading" />
</template>

<script lang="ts">
export default defineComponent({
    name: 'ShopsView',
    components: {
        EnsureLoggedIn,
        DatePicker,
        WeekViewer
    }
})
</script>
<style></style>
