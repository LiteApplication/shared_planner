<script setup lang="ts">
import { computed, defineComponent, onMounted, ref, type Ref } from 'vue';
import { shopApi } from '@/main';
import type { OpenRange, ShopWithOpenRange } from '@/api/types';
import DayTimeline from './DayTimeline.vue';
import { useI18n } from 'vue-i18n';
import { timeToMinutes } from '../utils';
import { type Task } from '../types';

const $t = useI18n().t;

</script>
<template>
    <div v-if="shopData">
        <h1>WeekViewer</h1>
        <p>Shop ID: {{ shopId }}</p>
        <p>Week Number: {{ weekNumber }}</p>
        <p>Shop name: {{ shopData.name }}</p>
        <div class="weekview">
            <DayTimeline v-for="day in Array(7).keys()" :key="day" :title="$t(`day.${day}`)" :tasks="shopData.open_ranges.filter(
                (range: OpenRange) => range.day === day
            ).map(
                (range: OpenRange) => ({
                    start_time: timeToMinutes(range.start_time),
                    end_time: timeToMinutes(range.end_time),
                    color: 'gray',
                    title: null,
                    description: $t('message.shop_open'),
                    id: range.id
                })) as Task[]
                " :startOfDay="dayBounds.start_time" :endOfDay="dayBounds.end_time" />
        </div>
    </div>
</template>

<script lang="ts">
export default defineComponent({
    name: 'WeekViewer',
    components: {
        DayTimeline
    },
    props: {
        shopId: {
            type: Number,
            required: true
        },
        year: {
            type: Number,
            required: true
        },
        weekNumber: {
            type: Number,
            required: true
        },
    },
    data() {
        return {
            shopData: null as ShopWithOpenRange | null,
            dayBounds: { start_time: timeToMinutes('12:00'), end_time: timeToMinutes('13:00') }
        };
    },
    mounted() {
        this.fetchShop(this.shopId);
    },
    methods: {
        async fetchShop(shopId: number) {
            shopApi.get(shopId).then(
                (shop) => {
                    console.log("Shop data", shop);
                    this.shopData = shop;
                    this.dayBounds = this.shopData.open_ranges.reduce(
                        (acc: { start_time: number, end_time: number }, range: OpenRange) => {
                            if (timeToMinutes(range.start_time) < acc.start_time) acc.start_time = timeToMinutes(range.start_time);
                            if (timeToMinutes(range.end_time) > acc.end_time) acc.end_time = timeToMinutes(range.end_time);
                            return acc;
                        },
                        { start_time: timeToMinutes('12:00'), end_time: timeToMinutes('13:00') }
                    );
                },
                error => {
                    if (error.response) console.log(error.response);
                    else
                        console.error(error);
                }
            );
        }
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