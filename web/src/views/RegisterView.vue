<script setup>
import { useI18n } from 'vue-i18n';
import { ref } from 'vue';
import { defineComponent } from 'vue'

import { useRouter } from 'vue-router';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import Select from 'primevue/select';
import Button from 'primevue/button';
import Card from 'primevue/card';


import { authApi } from '@/main';

const { t: $t } = useI18n();


const email = ref('');
const full_name = ref('');
const password = ref('');
const error_msg = ref('');
const group = ref('');
const router = useRouter();

const groups = [
    { name: 'MAGEV', code: 'MAGEV' }, { name: 'TOTAL', code: 'TOTAL' }, { name: 'ADA', code: 'ADA' }, { name: 'CBRE', code: 'CBRE' }, { name: 'SalesForce', code: 'SalesForce' }, { name: 'ABEILLE', code: 'ABEILLE' },
];

const onSubmit = async () => {
    if (email.value === '' || password.value === '' || full_name.value === '' || group.value === '') {
        error_msg.value = $t('error.fields');
        return;
    }
    authApi.register(email.value, password.value, full_name.value).then(
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
    <div class="register-container">

        <Card class="register-card">
            <template #title>{{ $t("message.register") }}</template>
            <template #content>
                <div class="fields">

                    <div class="flex flex-col gap-2">
                        <label for="email">{{ $t("message.email") }}</label>
                        <InputText id="email" v-model="email" />
                    </div>
                    <div class="flex flex-col gap-2">
                        <label for="full_name">{{ $t("message.full_name") }}</label>
                        <InputText id="full_name" v-model="full_name" />
                    </div>

                    <div class="flex flex-col gap-2">
                        <label for="full_name">{{ $t("message.group") }}</label>
                        <Select v-model="group" inputId="group" :options="groups" optionLabel="name" class="w-full" />
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
                    <Button v-bind:label="$t('message.to_login')" severity="secondary" outlined class="w-2/3" v-on:click="$router.push('/login')" />
                    <Button v-bind:label="$t('message.register')" class="w-1/3" v-on:click="onSubmit" />
                </div>
            </template>
        </Card>
    </div>
</template>

<script>



export default defineComponent({
    name: 'registerView',
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
.register-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.register-card {
    padding: 1.5rem;
    width: 30rem;
}

@media (max-width: 768px) {
    .register-card {
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
