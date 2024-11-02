<template>
    <Card style="width: 25rem; overflow: hidden" class="h-full">
        <template #title>
            <h2 class="text-xl font-semibold align-middle" v-if="shop.id != -1">{{ shop.name }}</h2>
            <Skeleton width="10rem" height="1.5rem" v-else></Skeleton>
        </template>

        <template #subtitle>
            <p class="text-xl font-normal" v-if="shop.id != -1"> {{ shop.location }}</p>
            <Skeleton width=" 8rem" height="1rem" v-else></Skeleton>
        </template>
        <template #content>
            <div class="">

                <p class="text-s font-bold mt-2 " v-if="shop.id != -1">
                    {{ $t('message.shops.description', {
                        from: formatDate(shop.available_from, $t('date_locale')), until: formatDate(shop.available_until, $t('date_locale')), volunteers:
                            shop.volunteers
                    }) }}
                </p>
                <Skeleton class="mt-2" width="25rem" height="1rem" v-else></Skeleton>
                <p class="text-s font-normal mt-2 text-red-500 whitespace-pre-line" v-if="shop.id != -1">
                    {{ shop.description }}
                </p>
            </div>

        </template>
        <template #footer>
            <div class="flex gap-4 mt-1">

                <Button :icon="PrimeIcons.MAP_MARKER" severity="secondary" aria-label="Bookmark" as="a" :href="shop.maps_link" target="_blank"
                    v-if="shop.id != -1" class="w-full" :label="$t('message.google_maps')" />
                <Button :icon="PrimeIcons.CALENDAR" class="p-1 w-full" :label="$t('message.shops.book')" v-if="shop.id != -1"
                    @click="router.push({ name: 'shop', params: { id: shop.id, week: getMonday(new Date()) } })" />
            </div>
        </template>

    </Card>
</template>

<script setup lang="ts">
import type { Shop } from '@/api/types';
import Skeleton from 'primevue/skeleton';
import { defineComponent, type PropType } from 'vue';
import { useI18n } from 'vue-i18n';
import { PrimeIcons } from '@primevue/core/api';
import Button from 'primevue/button';
import { getMonday, formatDate } from '@/utils';
import { useRouter } from 'vue-router';
import Card from 'primevue/card';

defineProps({
    shop: {
        type: Object as PropType<Shop>,
        required: true
    }
});

const $t = useI18n().t;
const router = useRouter();

</script>

<script lang="ts">
export default defineComponent({
    name: 'ShopItem',
    components: {
        Skeleton,
        // eslint-disable-next-line vue/no-reserved-component-names
        Button,
        Card
    }
})

</script>