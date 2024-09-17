<script setup lang="ts">
import Menubar from 'primevue/menubar';
import { defineComponent, onMounted, ref } from 'vue';
import { PrimeIcons } from '@primevue/core/api';
import { useI18n } from 'vue-i18n';
import { authApi, notificationsApi } from '@/main';
import { useRouter } from 'vue-router';
import Button from 'primevue/button';
import LocaleChanger from './LocaleChanger.vue';

const $t = useI18n().t;
const router = useRouter();

const logout = () => {
    authApi.logout();
    router.push('/login');
};


const notificationModel = defineModel('notificationCount');

const props = defineProps({
    isAdmin: Boolean
})


onMounted(() => {
    // Fetch notification count
    notificationsApi.count().then(
        (r) => {
            notificationModel.value = r;
        }
    ).catch(
        (e) => {
            console.error("Failed to fetch notification count", e);
        }
    );
});

const items = ref<any>([
    {
        label: $t("menu.my_reservations"),
        icon: PrimeIcons.CALENDAR,
        route: "/reservations"
    },
    {
        label: $t("menu.create_reservation"),
        icon: PrimeIcons.PLUS,
        route: "/shops"
    }
]);

const adminItems = ref(
    {
        label: $t("menu.admin.title"),
        icon: PrimeIcons.COG,
        items: [
            {
                label: $t("menu.admin.users"),
                icon: PrimeIcons.USERS,
                route: "/admin/users"
            },
            {
                label: $t("menu.admin.shops"),
                icon: PrimeIcons.BUILDING,
                route: "/admin/shops"
            },
            {
                label: $t("menu.admin.reservations"),
                icon: PrimeIcons.CALENDAR,
                route: "/admin/reservations"
            },
            {
                label: $t("menu.admin.settings"),
                icon: PrimeIcons.FILE_EDIT,
                route: "/admin/settings"
            }
        ]
    }
);
if (props.isAdmin)
    items.value.push(adminItems);


</script>

<template>
    <Menubar :model="items" class="m-4">
        <template #start>
            <img src="../assets/logo.png" alt="Logo" class="p-mr-2 h-12" />
        </template>
        <template #item="{ item, props, hasSubmenu }">
            <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
                <a v-ripple :href="href" v-bind="props.action" @click="navigate">
                    <span :class="item.icon" />
                    <span class="ml-1">{{ item.label }}</span>
                </a>
            </router-link>
            <a v-else v-ripple :href="item.url" :target="item.target" v-bind="props.action">
                <span :class="item.icon" />
                <span class="ml-1">{{ item.label }}</span>
                <span v-if="hasSubmenu" class="pi pi-fw pi-angle-down" />
            </a>
        </template>
        <!-- Logout button at the end -->
        <template #end>
            <div class="flex items-center gap-2">
                <Button :icon="PrimeIcons.BELL" :severity="notificationModel == 0 ? 'secondary' : 'info'" :text="notificationModel == 0"
                    :badge="notificationModel ? notificationModel.toString() : null" @click="router.push('/notifications')" />
                <LocaleChanger />
                <Button :label="$t('message.logout')" rounded icon="pi pi-sign-out" @click="logout" severity="danger" outlined />
            </div>
        </template>

    </Menubar>
</template>

<script lang="ts">
export default defineComponent({
    name: 'MainMenu',
    components: {
        Menubar,
        // eslint-disable-next-line vue/no-reserved-component-names
        Button,
        LocaleChanger,
    }
})
</script>
