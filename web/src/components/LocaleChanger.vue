<script setup lang="ts">
import { defineComponent } from 'vue';
import { languages } from '@/language';
</script>
<template>
    <div class="locale-changer">
        <select v-model="$i18n.locale">
            <option v-for="locale in $i18n.availableLocales" :key="`locale-${locale}`" :value="locale">{{ languages[locale] }}</option>
        </select>
    </div>
</template>

<script lang="ts">
export default defineComponent({
    name: 'LocaleChanger',
})
</script>