<script setup>
import { useI18n } from 'vue-i18n';
import { ref } from 'vue';
import { defineComponent } from 'vue'

import { useRouter } from 'vue-router';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Button from 'primevue/button';
import Card from 'primevue/card';


import { authApi } from '@/main';

const { t: $t } = useI18n();


const email = ref('');
const password = ref('');
const error_msg = ref('');
const router = useRouter();

const onSubmit = async () => {
    if (email.value === '' || password.value === '') {
        error_msg.value = $t('error.fields');
        return;
    }
    authApi.login(email.value, password.value).then(
        () => {
            console.log('Logged in');
            router.push('/');
        }
    ).catch(
        error => {
            if (error.response) {

                error_msg.value = $t(error.response.data.detail);
                password.value = '';
                console.log(error.response.data)
            } else {
                error_msg.value = $t('error.unknown');
                console.error(error);
            }

        }
    );
};



</script>

<template>
    <div class="login-container">

        <Card class="login-card">
            <template #title>{{ $t("message.login") }}</template>
            <template #content>
                <div class="fields">

                    <div class="flex flex-col gap-2">
                        <label for="email">{{ $t("message.email") }}</label>
                        <InputText id="email" v-model="email" />
                    </div>

                    <div class="flex flex-col gap-2">
                        <label for="password">{{ $t("message.password") }}</label>
                        <Password v-model="password" :feedback="false" id="password" />
                    </div>
                </div>

            </template>
            <template #footer>
                <p class="error" v-if="error_msg != '' && password == ''"> {{ error_msg }}</p>
                <div class="flex gap-4 mt-1">
                    <Button v-bind:label="$t('message.to_register')" severity="secondary" outlined class="w-2/3"
                        v-on:click="$router.push('/register')" />
                    <Button v-bind:label="$t('message.login')" class="w-1/3" v-on:click="onSubmit" />
                </div>
            </template>
        </Card>
    </div>
</template>

<script>



export default defineComponent({
    name: 'LoginView',
    components: {
        InputText,
        Password,
        // eslint-disable-next-line vue/no-reserved-component-names
        Button,
        Card,
    },
});
</script>

<style scoped>
.login-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.login-card {
    padding: 1.5rem;
    width: 30rem;
}

@media (max-width: 768px) {
    .login-card {
        width: 100%;
    }
}

.p-field {
    margin-top: 1.6 rem;
}

.error {
    color: rgb(255, 81, 81);
}
</style>
