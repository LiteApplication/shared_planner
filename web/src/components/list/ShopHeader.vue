<template>
    <div class="bg-slate-200 dark:bg-slate-700 rounded-lg m-4 p-3 ">
        <div class="flex justify-between items-center flex-wrap">

            <div class="flex flex-col">
                <div class="flex flex-row gap-2 items-center">
                    <Button :icon="PrimeIcons.MAP_MARKER" severity=" info" rounded outlined aria-label="Bookmark" as="a" :href="shop.maps_link"
                        target="_blank" v-if="shop.id != -1" />
                    <Skeleton shape="circle" size="2rem" class="mr-2" v-else></Skeleton>

                    <h2 class="text-xl font-semibold align-middle" v-if="shop.id != -1">{{ shop.name }}</h2>
                    <Skeleton width="10rem" height="1.5rem" v-else></Skeleton>
                    -
                    <p class="text-xl font-normal" v-if="shop.id != -1"> {{ shop.location }}</p>
                    <Skeleton width=" 8rem" height="1rem" v-else></Skeleton>
                </div>
                <p class="text-s font-normal mt-2" v-if="shop.id != -1">
                    {{ $t('message.shops.description_plain', {
                        from: formatDate(shop.available_from, $t('date_locale')), until: formatDate(shop.available_until, $t('date_locale')), volunteers:
                            shop.volunteers
                    }) }}
                </p>
                <Skeleton class="mt-2" width="25rem" height="1rem" v-else></Skeleton>
            </div>
            <div>
                <slot name="action"> </slot>
            </div>
        </div>
        <p v-if="shop.id != -1">{{ shop.description }}</p>
        <Skeleton class="mt-2" width="50%" height="1rem" v-else></Skeleton>
    </div>
</template>

<script setup lang="ts">
import type { Shop } from '@/api/types';
import Skeleton from 'primevue/skeleton';
import { defineComponent, type PropType } from 'vue';
import { useI18n } from 'vue-i18n';
import { PrimeIcons } from '@primevue/core/api';
import Button from 'primevue/button';
import { formatDate } from '@/utils';

defineProps({
    shop: {
        type: Object as PropType<Shop>,
        required: true
    }
});

const $t = useI18n().t;

</script>

<script lang="ts">
export default defineComponent({
    name: 'ShopHeader',
    components: {
        Skeleton,
        // eslint-disable-next-line vue/no-reserved-component-names
        Button
    }
})

</script>