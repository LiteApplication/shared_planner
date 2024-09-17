<template>
    <LoadingScreen :visible="loadingModel || additionalLoading" />
    <MainMenu :is-admin="userModel && userModel.admin" v-model:notification-count="notificationCount" />
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n';
import { authApi } from '@/main';
import { useToast } from 'primevue/usetoast';
import { useRouter } from 'vue-router';
import { onMounted } from 'vue';
import LoadingScreen from './LoadingScreen.vue';
import { defineComponent } from 'vue';
import { loadUserFromSession, saveUserToSession } from '@/api';
import handleError from '@/error_handler';
import MainMenu from './MainMenu.vue';

const toast = useToast();
const $router = useRouter();
const $t = useI18n().t;


const userModel = defineModel("user", {
    type: Object,
    required: false
});
const loadingModel = defineModel("loading", {
    type: Boolean,
    required: false,
    default: true
});

const notificationCount = defineModel("notificationCount", {
    type: Number,
    required: false,
    default: 0
});

const props = defineProps({
    additionalLoading: {
        type: Boolean,
        required: false,
        default: false
    },
    requireAdmin: {
        type: Boolean,
        default: false
    }
});

async function fetchData() {
    authApi.me().then(
        (user) => {
            console.log("Logged in as", user);
            if (props.requireAdmin && !user.admin) {
                toast.add({ severity: 'error', summary: $t('error.title'), detail: $t('admin.unauthorized') });
                $router.push('/login');
                return;
            }
            saveUserToSession(user);
            userModel.value = user;
            loadingModel.value = false;
        },
        error => {
            if (error.response && error.response.status === 401) {
                $router.push('/login');
            } else {
                handleError(toast, $t, "error.unknown")(error);
            }
            loadingModel.value = false;

        }
    );
}


onMounted(() => {
    const user = loadUserFromSession();
    if (user) {
        userModel.value = user;
        loadingModel.value = false;
    } else {
        fetchData();
    }
});
</script>

<script lang="ts">
export default defineComponent({
    name: 'EnsureLoggedIn',
    components: {
        LoadingScreen
    }
});
</script>