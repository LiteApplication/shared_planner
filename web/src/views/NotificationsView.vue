<script setup lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import EnsureLoggedIn from '@/components/EnsureLoggedIn.vue';
import MainMenu from '@/components/MainMenu.vue';
import Timeline from 'primevue/timeline';
import { exampleNotification } from '@/api/types';
import type { Notification } from '@/api/types';
import { PrimeIcons } from '@primevue/core/api';
import { notificationsApi } from '@/main';
import Button from 'primevue/button';
import handleError from '@/error_handler';
import { useToast } from 'primevue/usetoast';

const toast = useToast();
const $t = useI18n().t;

const notifications = ref<Notification[]>([exampleNotification, exampleNotification, exampleNotification]);

const notifCount = ref(0);
const sorted = (r: Notification[]) => r.sort((a, b) => -((a.date > b.date) ? 1 : ((b.date > a.date) ? -1 : 0)))

onMounted(() => {
    notificationsApi.list().then(
        (r) => {
            notifications.value = sorted(r);
        }
    )
});


const getIcon = (notification: Notification) => {
    if (notification.icon != null) {
        return notification.icon;
    }
    if (notification.is_reminder) {
        return PrimeIcons.BELL;
    } else {
        return PrimeIcons.ENVELOPE;
    }
};

const getColor = (notification: Notification) => {
    if (notification.is_reminder) {
        return 'bg-teal-500 dark:bg-teal-400';
    } else {
        return 'bg-blue-500 dark:bg-blue-400';
    }
};


function deleteNotification(notif: Notification) {
    notificationsApi.delete(notif.id).catch(handleError(toast, $t));
    if (!notif.read) {
        notifCount.value -= 1;
    }
    notifications.value = sorted(notifications.value.filter(n => n.id !== notif.id));
}

function markAsRead(notif: Notification) {
    notificationsApi.mark_as_read(notif.id).then((r) => {
        notifications.value = sorted(notifications.value.map(n => n.id === notif.id ? r : n));
    }).catch(handleError(toast, $t));
    if (!notif.read) {
        notifCount.value -= 1;
    }
    notif.read = true;
}

function markAsUnread(notif: Notification) {
    notificationsApi.mark_as_unread(notif.id).then((r) => {
        notifications.value = sorted(notifications.value.map(n => n.id === notif.id ? r : n));
    }).catch(handleError(toast, $t));
    if (notif.read) {
        notifCount.value += 1;
    }
    notif.read = false;
}

function markAsReadAll() {
    notificationsApi.mark_all_as_read().then((r) => {
        notifications.value = sorted(r);
    }).catch(handleError(toast, $t));
    notifCount.value = 0;
    notifications.value.forEach(n => n.read = true);
}

</script>
<script lang="ts">
export default defineComponent({
    name: 'AdminSettingsView',
    components: {
        EnsureLoggedIn,
        Timeline,
        // eslint-disable-next-line vue/no-reserved-component-names
        Button
    }
})
</script>
<template>
    <EnsureLoggedIn v-model:notification-count="notifCount" />


    <Button :label="$t('notification.mark_all_as_read')" @click="markAsReadAll" :disabled="notifCount == 0"
        :severity="notifCount == 0 ? 'secondary' : 'info'" class="ml-4" :icon="PrimeIcons.CHECK_SQUARE" />
    <Timeline :value="notifications">
        <template #opposite="{ item }">
            <div class="text-surface-500 dark:text-surface-400">{{ (new Date(item.date)).toDateString() }}</div>
        </template>
        <template #content="{ item }">
            <div class="flex flex-col flex-shrink">
                <h3>{{ $t(item.message + ".title", JSON.parse(item.data)) }}</h3>
                <p>{{ $t(item.message + ".body", JSON.parse(item.data)) }}</p>

                <div class="flex flex-row">
                    <Button :icon="PrimeIcons.TRASH" text severity="danger" :label="$t('notification.delete')" @click="deleteNotification(item)" />
                    <Button :icon="PrimeIcons.FILE_EXPORT" text severity="primary" :label="$t(item.message + '.access')"
                        @click="$router.push(item.route)" v-if="item.route != null" />
                    <Button :icon="PrimeIcons.CHECK_SQUARE" text severity="info" :label="$t('notification.mark_as_unread')"
                        @click="markAsUnread(item)" v-if="item.read" />
                    <Button :icon="PrimeIcons.STOP" text severity="info" :label="$t('notification.mark_as_read')" @click="markAsRead(item)" v-else />
                </div>
            </div>
        </template>

        <template #marker="slotProps">
            <span class="flex w-8 h-8 items-center justify-center text-white rounded-full z-2 shadow-sm" :class="getColor(slotProps.item)">
                <i :class="getIcon(slotProps.item)" />
            </span>
        </template>


    </Timeline>
</template>