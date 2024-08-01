import './assets/main.css'

import App from './App.vue'
import router from './router'
import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import { createI18n } from 'vue-i18n';
import messages from './language';

import AuthApi from './api/auth';
import Tooltip from 'primevue/tooltip';
import ShopApi from './api/shop';




const app = createApp(App);
app.use(PrimeVue, {
    theme: {
        preset: Aura
    }
});
app.use(router)
app.directive('tooltip', Tooltip);

const i18n = createI18n({
    legacy: false,
    locale: 'fr',
    messages
});

app.use(i18n);

app.mount('#app')

const authApi: AuthApi = new AuthApi();
const shopApi: ShopApi = new ShopApi();

export { authApi, shopApi };
