<script setup lang="ts">
import { defineComponent } from 'vue';
import { languages } from '@/language';
import { useI18n } from 'vue-i18n';
import { watch } from 'vue';
import { PrimeIcons } from '@primevue/core/api';
import { computed, ref } from 'vue';
import Select from 'primevue/select';
import Button from 'primevue/button';

const i18n = useI18n();

// Get the preferred language from the store
if (localStorage.getItem('locale') === null) {

    const browserLanguage = navigator.language.split('-')[0];

    if (Object.keys(languages).includes(browserLanguage)) {
        localStorage.setItem('locale', browserLanguage);
    } else {
        console.warn(`Language ${browserLanguage} not supported, falling back to fr-FR`);

        localStorage.setItem('locale', 'fr-FR');
    }
}

// Set the locale
const locale = localStorage.getItem('locale');

if (locale) {
    i18n.locale.value = locale;
}

watch(() => i18n.locale.value, (newLocale) => {
    localStorage.setItem('locale', newLocale);
});

const locales = computed(() => i18n.availableLocales.map((locale) => ({ label: languages[locale], value: locale })));

const showLanguages = ref(false);

</script>
<template>
    <div class="locale-changer">
        <Select v-model="$i18n.locale" :options="locales" optionLabel="label" optionValue="value" v-if="showLanguages" />
        <Button text :icon="PrimeIcons.LANGUAGE" severity="secondary" @click="showLanguages = !showLanguages" v-else />
    </div>
</template>

<script lang="ts">
export default defineComponent({
    name: 'LocaleChanger',
    components: {
        // eslint-disable-next-line vue/no-reserved-component-names
        Select,
        // eslint-disable-next-line vue/no-reserved-component-names
        Button
    }
})
</script>