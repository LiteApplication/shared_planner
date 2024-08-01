<script setup lang="ts">
import { defineComponent, onMounted, ref, type Ref } from 'vue';
import { shopApi } from '@/main';
import type { OpenRange, ShopWithOpenRange } from '@/api/types';
import DayTimeline from './DayTimeline.vue';

</script>
<template>
    <div v-if="shopData">
        <h1>WeekViewer</h1>
        <p>Shop ID: {{ shopId }}</p>
        <p>Week Number: {{ weekNumber }}</p>
        <p>Shop name: {{ shopData.name }}</p>
        <div class="weekview">
            <DayTimeline v-for="day in Array(7).keys()" :key="day" :title="`${shopData.name}: ${day}`" :tasks="shopData.open_ranges.filter(
                (range: OpenRange) => range.day === day
            ).map(
                (range: OpenRange) => ({
                    start_time: range.start_time,
                    end_time: range.end_time,
                    color: 'gray',
                    tooltip: null
                })
            )" startOfDay="08:00" endOfDay="20:00" />
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
        weekNumber: {
            type: Number,
            required: true
        },
    },
    data() {
        return {
            shopData: null as ShopWithOpenRange | null
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
                },
                error => {
                    if (error.response) console.log(error.response);
                    else
                        console.error(error);
                }
            );
        }
    }
});
</script>