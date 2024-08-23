<template>
    <LoadingScreen :visible="loadingModel || additionalLoading" />
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

defineProps({
    additionalLoading: {
        type: Boolean,
        required: false,
        default: false
    }
});

async function fetchData() {
    authApi.me().then(
        (user) => {
            console.log("Logged in as", user);
            saveUserToSession(user);
            userModel.value = user;
            loadingModel.value = false;
        },
        error => {
            if (error.response && error.response.status === 401) {
                $router.push('/login');
            } else {
                console.error(error);
                if (error.response == undefined) {
                    toast.add({ severity: 'error', summary: $t('error.title'), detail: $t('error.unknown') });
                } else
                    if (error.response.data.detail) {
                        toast.add({ severity: 'error', summary: $t('error.title'), detail: $t(error.response.data.detail) });
                    } else {
                        toast.add({ severity: 'error', summary: $t('error.title'), detail: $t('error.unknown') });
                    }
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