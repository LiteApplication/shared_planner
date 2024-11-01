<template>
    <EnsureLoggedIn require-admin :additional-loading="loading" />
    <Toolbar class="mx-4">
        <template #start>
            <Select v-model="selectedShopInList" :options="shops" optionLabel="name" @change="loadShopDetails" checkmark class="m-1" showClear />
            <Button :label="$t('admin.shop.create')" icon="pi pi-plus" @click="addShop" class="m-1 w-full" />
        </template>
        <template #end>
            <Button :label="$t('admin.shop.delete')" icon="pi pi-trash" class="m-1" v-if="selectedShop" severity="danger" @click="onDeleteShop" />
        </template>
    </Toolbar>
    <div v-if="selectedShop" class="m-4">
        <form @submit.prevent="saveShop">
            <div class="flex gap-4 flex-wrap justify-center">
                <div class="flex flex-col gap-4">
                    <Panel class="flex-grow">
                        <template #header>
                            <div class="flex justify-between w-full">
                                <h2 class="text-lg font-bold">{{ $t('admin.shop.informations') }}</h2>
                                <Button :label="$t('message.save')" icon="pi pi-save" type="submit" />
                            </div>
                        </template>
                        <div class="flex flex-col gap-2 pt-6">
                            <IftaLabel>
                                <label for="name">{{ $t('admin.shop.name') }}</label>
                                <InputText id="name" v-model="selectedShop.name" fluid />
                            </IftaLabel>
                            <IftaLabel>
                                <label for="description">{{ $t("admin.shop.description") }}</label>
                                <Textarea id="description" v-model="selectedShop.description" fluid />
                            </IftaLabel>
                            <IftaLabel>
                                <label for="location">{{ $t("admin.shop.location") }}</label>
                                <InputText id="location" v-model="selectedShop.location" fluid />
                            </IftaLabel>
                            <IftaLabel>
                                <label for="maps_link">{{ $t("admin.shop.maps") }}</label>
                                <InputText id="maps_link" v-model="selectedShop.maps_link" fluid />
                            </IftaLabel>
                            <div class="flex gap-4 flex-wrap">
                                <IftaLabel class="flex-grow">
                                    <InputNumber id="volunteers" v-model="selectedShop.volunteers" fluid />
                                    <label for="volunteers">{{ $t("admin.shop.volunteers") }}</label>
                                </IftaLabel>
                                <IftaLabel class="flex-grow">
                                    <InputNumber id="min_time" v-model="selectedShop.min_time" fluid />
                                    <label for="min_time">{{ $t("admin.shop.min_time") }}</label>
                                </IftaLabel>
                                <IftaLabel class="flex-grow">
                                    <InputNumber id="max_time" v-model="selectedShop.max_time" fluid />
                                    <label for="max_time">{{ $t("admin.shop.max_time") }}</label>
                                </IftaLabel>
                            </div>
                            <div class="flex flex-wrap gap-2 flex-grow justify-between">
                                <IftaLabel>
                                    <DatePicker id="available_from" v-model="startDate" v-if="selectedShop !== null" inline date-format="yy-mm-dd" />
                                    <label for="available_from">{{ $t("admin.shop.start_date") }}</label>
                                </IftaLabel>
                                <IftaLabel>
                                    <DatePicker id="available_until" v-model="endDate" v-if="selectedShop !== null" inline date-format="yy-mm-dd" />
                                    <label for="available_until">{{ $t("admin.shop.end_date") }}</label>
                                </IftaLabel>
                            </div>
                        </div>
                    </Panel>
                </div>
                <Panel :header="$t('admin.shop.open_ranges')">
                    <template #header>
                        <div class="flex justify-between w-full">
                            <h2 class="text-lg font-bold">{{ $t('admin.shop.open_ranges') }}</h2>
                            <Button icon="pi pi-plus" outlined :label="$t('admin.shop.or_add')" class="" @click="addOpenRange"
                                v-if="selectedShop.id !== -1" />
                        </div>
                    </template>
                    <DataTable :value="selectedShop.open_ranges" dataKey="id" tableStyle="" resizableColumns columnResizeMode="fit" size="large"
                        stripedRows sort-field="day" :sort-order="1" removableSort v-if="'open_ranges' in selectedShop" edit-mode="row"
                        v-model:editingRows="editingRowsOR" @row-edit-save="onOpenRangeSave">
                        <Column field="day" :header="$t('admin.shop.or_day')" sortable>
                            <template #editor="{ data }">
                                <Select v-model="data.day" optionValue="value"
                                    :options="Array.from({ length: 7 }, (_, index) => ({ label: $t('day.' + index), value: index }))"
                                    optionLabel="label" :invalid="data.day === null" />
                            </template>
                            <template #body="{ data }">
                                {{ $t('day.' + data.day) }}
                            </template>
                        </Column>
                        <Column field="start_time" :header="$t('admin.shop.or_start')" sortable>
                            <template #editor="{ data }">
                                <InputMask v-model="data.start_time" mask="99:99" placeholder="HH:MM" :invalid="!validTime(data.start_time)" />
                            </template>
                        </Column>
                        <Column field="end_time" :header="$t('admin.shop.or_end')" sortable>
                            <template #editor="{ data }">
                                <InputMask v-model="data.end_time" mask="99:99" placeholder="HH:MM" :invalid="!validTime(data.end_time)" />
                            </template>
                        </Column>
                        <Column rowEditor style="width: 10%; min-width: 8rem" bodyStyle="text-align:center"></Column>
                        <Column style="width: 10%; min-width: 4rem">
                            <template #body="{ data }">
                                <Button icon="pi pi-trash" class="p-button-rounded p-button-danger p-button-text" @click="deleteOpenRange(data.id)" />
                            </template>
                        </Column>
                    </DataTable>
                </Panel>
            </div>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { type OpenRange, type Shop, type ShopWithOpenRange, exampleShop } from '@/api/types';
import { shopApi } from '@/main';
import EnsureLoggedIn from '@/components/EnsureLoggedIn.vue';
import Select from 'primevue/select';
import Button from 'primevue/button';
import { useToast } from 'primevue/usetoast';
import { useI18n } from 'vue-i18n';
import DatePicker from '@/components/primevue/DatePicker';
import Column from 'primevue/column';
import DataTable from 'primevue/datatable';
import InputNumber from 'primevue/inputnumber';
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';
import IftaLabel from 'primevue/iftalabel';
import Panel from 'primevue/panel';
import Toolbar from 'primevue/toolbar';
import { networkDate } from '@/utils';
import InputMask from 'primevue/inputmask';
import handleError from '@/error_handler';
import { invalidateCache } from '@/api';
const toast = useToast();
const $t = useI18n().t;

const shops = ref<Shop[]>([]);
const selectedShopInList = ref<Shop | null>(null);
const selectedShop = ref<ShopWithOpenRange | null>(null);
const loading = ref(false);

const editingRowsOR = ref<OpenRange[]>([]);



const startDate = ref<Date | null>(null);
const endDate = ref<Date | null>(null);

function validTime(time: string) {
    return time.match(/^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$/);
}


function loadList() {
    loading.value = true;
    invalidateCache();

    shopApi.list().then(
        (r) => {
            shops.value = r;
            selectedShopInList.value = r[shops.value.length - 1];
            loadShopDetails();
        }
    ).catch(handleError(toast, $t, "error.shop.unknown")).finally(() => loading.value = false);
}

function loadShopDetails() {
    if (selectedShopInList.value) {
        loading.value = true;
        shopApi.get(selectedShopInList.value.id).then(
            (r) => {
                startDate.value = new Date(r.available_from);
                endDate.value = new Date(r.available_until);
                // All open ranges are converted to the correct format HH:MM
                r.open_ranges = r.open_ranges.map((o) => ({ ...o, start_time: o.start_time.substring(0, 5), end_time: o.end_time.substring(0, 5) }));
                selectedShop.value = r;

                loading.value = false;

            }
        ).catch(handleError(toast, $t, "error.shop.unknown"));
    } else {
        selectedShop.value = null;
    }
}

function addShop() {
    selectedShop.value = { ...exampleShop, open_ranges: [] };
    selectedShopInList.value = selectedShop.value;
}

function addOpenRange() {
    if (selectedShop.value) {
        selectedShop.value.open_ranges.push({ id: -1, day: 0, start_time: '00:00', end_time: '00:00' });
        editingRowsOR.value.push(selectedShop.value.open_ranges[selectedShop.value.open_ranges.length - 1]);
    }
}

function onOpenRangeSave(event: { newData: OpenRange, data: OpenRange, index: number }) {
    const { newData, data, index } = event;
    invalidateCache();

    selectedShop.value!.open_ranges[index] = newData; // optimistic update

    if (newData.id === -1) {
        shopApi.addOpenRange(selectedShop.value!.id, newData).then(
            (r) => {
                selectedShop.value = r;
                toast.add({ severity: 'success', summary: $t("message.success"), detail: $t("admin.shop.or_added") });
            }
        ).catch(handleError(toast, $t)).finally(
            loadShopDetails
        );
    } else {
        shopApi.updateOpenRange(newData).then(
            (r) => {
                selectedShop.value = r;
                toast.add({ severity: 'success', summary: $t("message.success"), detail: $t("admin.shop.or_updated") });
            }
        ).catch(handleError(toast, $t)).finally(
            loadShopDetails
        );
    }
}

function deleteOpenRange(id: number) {
    invalidateCache();
    shopApi.deleteOpenRange(id).then(
        () => {
            toast.add({ severity: 'success', summary: $t("message.success"), detail: $t("admin.shop.or_deleted") });
        }
    ).catch(handleError(toast, $t));

    selectedShop.value!.open_ranges = selectedShop.value!.open_ranges.filter((o) => o.id !== id);

}

function saveShop() {
    if (!selectedShop.value) {
        return;
    }
    selectedShop.value.available_from = networkDate(startDate.value!);
    selectedShop.value.available_until = networkDate(endDate.value!);

    if (selectedShop.value.id === -1) {
        shopApi.create(selectedShop.value).then(
            (r) => {
                loadList();
                selectedShopInList.value = r;
                toast.add({ severity: 'success', summary: $t("message.success"), detail: $t("admin.shop.created") });
            }
        ).catch(handleError(toast, $t));
        return;
    }

    invalidateCache();
    shopApi.update(selectedShop.value).then(
        () => {
            loadShopDetails();
            toast.add({ severity: 'success', summary: $t("message.success"), detail: $t("admin.shop.updated") });
        }
    ).catch(handleError(toast, $t));


}

function onDeleteShop() {
    if (!selectedShop.value) {
        return;
    }
    if (!confirm($t("admin.shop.delete_confirm"))) return;


    shopApi.delete(selectedShop.value.id).then(
        () => {
            loadList();
            toast.add({ severity: 'success', summary: $t("message.success"), detail: $t("admin.shop.deleted") });
        }
    ).catch(handleError(toast, $t));

    selectedShop.value = null;
    shops.value = shops.value.filter((s) => s.id !== selectedShopInList.value!.id);
    selectedShopInList.value = null;
}

onMounted(loadList);
</script>

<script lang="ts">
export default {
    name: 'AdminShopsView',
    components: {
        EnsureLoggedIn,
        // eslint-disable-next-line vue/no-reserved-component-names
        Select,
        // eslint-disable-next-line vue/no-reserved-component-names
        Button,
        InputText,
        // eslint-disable-next-line vue/no-reserved-component-names
        Textarea,
        InputMask,
        DatePicker,
        DataTable,
        Column,
        IftaLabel,
        Panel,
        Toolbar
    },
}
</script>
