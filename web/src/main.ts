import './assets/main.scss'

import App from './App.vue'
import router from './router'
import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import Aura from '@primevue/themes/aura';
import { createI18n } from 'vue-i18n';
import messages from './language';
import Tooltip from 'primevue/tooltip';
import ToastService from 'primevue/toastservice';
import Ripple from 'primevue/ripple';

import AuthApi from './api/auth';
import ShopApi from './api/shop';
import ReservationApi from './api/reservation';



const app = createApp(App);
app.use(PrimeVue, {
    theme: {
        preset: Aura,
        ripple: true,
    }
});
app.use(router)
app.directive('tooltip', Tooltip);
app.use(ToastService);
app.directive('ripple', Ripple);

const i18n = createI18n({
    legacy: false,
    locale: 'en',
    messages
});

app.use(i18n);

app.mount('#app')

const authApi: AuthApi = new AuthApi();
const shopApi: ShopApi = new ShopApi();
const reservationApi: ReservationApi = new ReservationApi();

export { authApi, shopApi, reservationApi };
