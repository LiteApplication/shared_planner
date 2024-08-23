<script setup lang="ts">

import { defineComponent, onMounted, ref, type Ref } from 'vue'
import { useRouter } from 'vue-router';

import { useToast } from 'primevue/usetoast';
import { useI18n } from 'vue-i18n';
import EnsureLoggedIn from '@/components/EnsureLoggedIn.vue';
import MainMenu from '@/components/MainMenu.vue';
import ShopItem from '@/components/list/ShopItem.vue';
import { exampleShop, type Shop } from '@/api/types';
import { shopApi } from '@/main';

const $router = useRouter();
const toast = useToast();
const $t = useI18n().t;

const shops: Ref<Shop[]> = ref([
    exampleShop,
    exampleShop,
]);

onMounted(() => {
    shopApi.list().then(
        (r) => { shops.value = r }
    )
}
)



</script>
<template>
    <EnsureLoggedIn />
    <MainMenu />
    <div>
        <ShopItem v-for="(shop, index) in shops" :key="shop.id === -1 ? index : shop.id" :shop="shop" />
    </div>
</template>

<script lang="ts">
export default defineComponent({
    name: 'ShopsView',
    components: {
        EnsureLoggedIn,
        MainMenu,
        ShopItem
    }
})
</script>
<style></style>