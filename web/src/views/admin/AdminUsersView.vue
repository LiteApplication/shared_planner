<template>
    <EnsureLoggedIn require-admin />
    <DataTable :value="users" dataKey="id" tableStyle="min-width: 60rem" size="large" stripedRows sort-field="group" :sort-order="1" removableSort
        :globalFilterFields="['full_name', 'email', 'group']" filterDisplay="row" v-model:filters="filters" editMode="row" @row-edit-save="saveRow"
        v-model:editingRows="editingRows" @row-edit-init="onRowEditInit" @row-edit-cancel="editingRows = []" v-model:selection="selectedUsers">
        <template #header>
            <Toolbar>
                <template #start>
                    <div class="flex gap-2">
                        <Button label="Add" icon="pi pi-plus" @click="addUser" />
                        <Button label="Delete" icon="pi pi-trash" class="p-button-danger" @click="confirmDeleteSelectedUsers"
                            :disabled="!selectedUsers.length" />
                    </div>
                </template>
                <template #end>
                    <IconField>
                        <InputIcon>
                            <i class=" pi pi-search" />
                        </InputIcon>
                        <InputText v-model="filters['global'].value" placeholder="Keyword Search" />
                    </IconField>
                </template>
            </Toolbar>
        </template>
        <template #empty>
            <div class="p-4">
                <p>No users found.</p>
            </div>
        </template>
        <Column selectionMode="multiple" header-style="width: 3em"></Column>
        <Column field="full_name" :header="$t('message.full_name')" sortable>
            <template #editor>
                <InputText v-model="editField_full_name" />
            </template>
        </Column>
        <Column field="email" :header="$t('message.email')" sortable>
            <template #editor>
                <InputText v-model="editField_email" mode="email" />
            </template>
        </Column>
        <Column field="group" :header="$t('message.group')" sortable>
            <template #editor>
                <InputText v-model="editField_group" />
            </template>
        </Column>

        <Column :header="$t('admin.admin_column')" field="admin" sortable data-type="boolean">
            <template #body="{ data }">
                <i class="pi" :class="{ 'pi-check-circle text-green-500': data.admin, 'pi-times-circle text-red-400': !data.admin }"></i>
            </template>
            <template #editor>
                <ToggleSwitch v-model="editField_admin" />
            </template>
        </Column>
        <Column row-editor style="width: 10%; min-width: 8rem" bodyStyle="text-align:center"></Column>
    </DataTable>
</template>

<script setup lang="ts">
import { exampleUser, type User } from '@/api/types';
import EnsureLoggedIn from '@/components/EnsureLoggedIn.vue';
import Button from 'primevue/button';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';
import { FilterMatchMode } from '@primevue/core/api';
import { defineComponent, onMounted, ref } from 'vue'
import ToggleSwitch from 'primevue/toggleswitch';
import { usersApi } from '@/main';
import { useToast } from 'primevue/usetoast';
import { useI18n } from 'vue-i18n';
import Toolbar from 'primevue/toolbar';
import handleError from '@/error_handler';

const toast = useToast();
const $t = useI18n().t;

const users = ref<User[]>([
    exampleUser,
    exampleUser,
    exampleUser,
]);

const filters = ref({
    global: { value: null, matchMode: FilterMatchMode.CONTAINS },
});

const editingRows = ref<User[]>([]);

const editField_full_name = ref('');
const editField_email = ref('');
const editField_group = ref('');
const editField_admin = ref(false);

const onRowEditInit = (e: any) => {
    editingRows.value = [e.data];
    editField_full_name.value = e.data.full_name;
    editField_email.value = e.data.email;
    editField_group.value = e.data.group;
    editField_admin.value = e.data.admin;
};

function loadList() {
    usersApi.list().then(
        (r) => {
            users.value = r;
        }
    ).catch(handleError(toast, $t));
}

const saveRow = (e: any) => {

    usersApi.update({
        id: e.data.id,
        full_name: editField_full_name.value,
        email: editField_email.value,
        group: editField_group.value,
        admin: editField_admin.value,
    }).then(loadList).catch(handleError(toast, $t));
    users.value = users.value.map(
        (u) => {
            if (u.id == e.data.id) {
                return {
                    id: e.data.id,
                    full_name: editField_full_name.value,
                    email: editField_email.value,
                    group: editField_group.value,
                    admin: editField_admin.value,
                }
            }
            return u;
        }
    );
};


const selectedUsers = ref<User[]>([]);

onMounted(loadList);

function addUser() {
    usersApi.create('', 'New User', '', '', false).then(loadList).catch(handleError(toast, $t));
}

// Function to confirm and delete selected users
const confirmDeleteSelectedUsers = () => {
    if (confirm($t('admin.confirm_delete_selected_users'))) {
        deleteSelectedUsers().then(
            () => {
                selectedUsers.value = [];
                toast.add({ severity: 'success', summary: $t("message.success"), detail: $t("admin.user_deleted") });
                loadList();
            }
        ).catch(handleError(toast, $t));

    }
};

// Function to delete selected users
const deleteSelectedUsers = async () => {
    const idsToDelete = selectedUsers.value.map(user => user.id);
    idsToDelete.forEach(async id => {
        await usersApi.delete(id);
    });
};

</script>

<script lang="ts">
export default defineComponent({
    name: 'AdminUsersView',
    components: {
        EnsureLoggedIn,
        DataTable,
        Column,
        IconField,
        InputIcon,
        InputText,
        ToggleSwitch,
        Toolbar
    },
})
</script>