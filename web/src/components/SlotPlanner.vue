<template>
    <div class="slot-planner-wrapper">
        <div class="flex items-center gap-3 mb-3">
            <p class="text-sm text-slate-500 dark:text-slate-400">{{ $t('admin.shop.slot_drag_hint') }}</p>
            <div class="flex items-center gap-2 ml-auto">
                <label class="text-sm" style="color: var(--p-text-muted-color)">{{ $t('admin.shop.slot_filter_date') }}</label>
                <DatePicker v-model="filterDate" showButtonBar showIcon :date-format="$t('message.shops.week_format')"
                    :placeholder="$t('message.all')" class="w-44" />
            </div>
        </div>
        <div class="slot-planner" @mouseleave="cancelDraw" @mouseup.prevent="endDraw">
            <!-- Time axis -->
            <div class="time-axis">
                <div class="day-header-placeholder"></div>
                <div class="time-labels">
                    <div v-for="h in visibleHours" :key="h" class="time-label" :style="timeAxisStyle(h)">
                        {{ String(h).padStart(2, '0') }}:00
                    </div>
                </div>
            </div>
            <!-- Day columns -->
            <div class="days-area">
                <div v-for="day in 7" :key="day - 1" class="day-col">
                    <div class="day-header">{{ $t('day.' + (day - 1)) }}</div>
                    <div class="timeline-area" :ref="(el) => setTimelineRef(day - 1, el as HTMLElement)"
                        @mousedown.prevent="startDraw(day - 1, $event)"
                        @mousemove.prevent="onMouseMove(day - 1, $event)">
                        <!-- Hour grid lines -->
                        <div v-for="h in visibleHours" :key="h" class="grid-line"
                            :style="{ top: minuteToPercent((h - DAY_START_H) * 60) + '%' }"></div>
                        <!-- Half-hour grid lines -->
                        <div v-for="h in visibleHours" :key="'h' + h" class="grid-line half"
                            :style="{ top: minuteToPercent((h - DAY_START_H) * 60 + 30) + '%' }"></div>

                        <!-- Existing slots for this day -->
                        <div v-for="slot in slotsForDay(day - 1)" :key="slot.id"
                            class="slot-block" :class="slotClass(slot)"
                            :style="slotStyle(slot)"
                            @dblclick.stop="openEditSlot(slot)"
                            @mousedown.stop>
                            <span class="slot-label">
                                {{ slot.start_time.slice(0, 5) }}–{{ slot.end_time.slice(0, 5) }}
                            </span>
                            <span class="slot-sub">{{ slot.max_volunteers }} pers.</span>
                        </div>

                        <!-- Draw preview -->
                        <div v-if="draw.active && draw.day === day - 1 && draw.startMin !== draw.endMin"
                            class="slot-preview"
                            :style="previewStyle"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <SlotEditDialog v-model:visible="editDialogVisible" :slot="editingSlot" :shopId="shopId"
        @save="onSlotSave" @delete="onSlotDelete" />
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue';
import type { TimeSlot } from '@/api/types';
import SlotEditDialog from './dialog/SlotEditDialog.vue';
import DatePicker from '@/components/primevue/DatePicker';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

const props = defineProps<{
    slots: TimeSlot[],
    shopId: number
}>();

const emit = defineEmits<{
    create: [slot: Partial<TimeSlot>],
    update: [slot: Partial<TimeSlot>],
    delete: [slotId: number]
}>();

const DAY_START_H = 6;   // 06:00
const DAY_END_H = 22;    // 22:00
const TOTAL_MINUTES = (DAY_END_H - DAY_START_H) * 60;

const visibleHours = computed(() => {
    const hours = [];
    for (let h = DAY_START_H; h <= DAY_END_H; h++) hours.push(h);
    return hours;
});

const filterDate = ref<Date | null>(new Date());

// Timeline element refs per day
const timelineRefs = ref<(HTMLElement | null)[]>(Array(7).fill(null));
function setTimelineRef(day: number, el: HTMLElement | null) {
    timelineRefs.value[day] = el;
}

// Draw state
const draw = reactive({ active: false, day: -1, startMin: 0, endMin: 0 });

// Edit dialog
const editDialogVisible = ref(false);
const editingSlot = ref<Partial<TimeSlot> | null>(null);

function minuteToPercent(minutes: number): number {
    return Math.max(0, Math.min(100, (minutes / TOTAL_MINUTES) * 100));
}

function timeAxisStyle(h: number) {
    return { top: minuteToPercent((h - DAY_START_H) * 60) + '%' };
}

function yToMinutes(y: number, el: HTMLElement): number {
    const rect = el.getBoundingClientRect();
    const relY = Math.max(0, Math.min(rect.height, y - rect.top));
    const raw = DAY_START_H * 60 + (relY / rect.height) * TOTAL_MINUTES;
    return Math.round(raw / 30) * 30;
}

function startDraw(day: number, e: MouseEvent) {
    const el = timelineRefs.value[day];
    if (!el) return;
    const min = yToMinutes(e.clientY, el);
    draw.active = true;
    draw.day = day;
    draw.startMin = min;
    draw.endMin = min + 60;
}

function onMouseMove(day: number, e: MouseEvent) {
    if (!draw.active || draw.day !== day) return;
    const el = timelineRefs.value[day];
    if (!el) return;
    const min = yToMinutes(e.clientY, el);
    draw.endMin = Math.max(draw.startMin + 30, min);
}

function endDraw() {
    if (!draw.active) return;
    const duration = draw.endMin - draw.startMin;
    if (duration >= 30) {
        const startH = Math.floor(draw.startMin / 60);
        const startM = draw.startMin % 60;
        const endH = Math.floor(draw.endMin / 60);
        const endM = draw.endMin % 60;
        editingSlot.value = {
            day: draw.day,
            start_time: `${String(startH).padStart(2, '0')}:${String(startM).padStart(2, '0')}:00`,
            end_time: `${String(endH).padStart(2, '0')}:${String(endM).padStart(2, '0')}:00`,
            max_volunteers: 1,
        };
        editDialogVisible.value = true;
    }
    draw.active = false;
    draw.day = -1;
}

function cancelDraw() {
    if (draw.active) {
        draw.active = false;
        draw.day = -1;
    }
}

function openEditSlot(slot: TimeSlot) {
    editingSlot.value = { ...slot };
    editDialogVisible.value = true;
}

function slotsForDay(day: number): TimeSlot[] {
    return props.slots.filter(s => {
        if (s.day !== day) return false;
        if (!filterDate.value) return true;
        const d = filterDate.value.toISOString().slice(0, 10);
        return s.valid_from <= d && s.valid_until >= d;
    });
}

function slotStartMin(slot: TimeSlot): number {
    const [h, m] = slot.start_time.split(':').map(Number);
    return h * 60 + m - DAY_START_H * 60;
}

function slotEndMin(slot: TimeSlot): number {
    const [h, m] = slot.end_time.split(':').map(Number);
    return h * 60 + m - DAY_START_H * 60;
}

function slotStyle(slot: TimeSlot) {
    const top = minuteToPercent(slotStartMin(slot));
    const height = minuteToPercent(slotEndMin(slot) - slotStartMin(slot));
    return { top: `${top}%`, height: `${height}%` };
}

function slotClass(slot: TimeSlot) {
    const today = new Date().toISOString().slice(0, 10);
    if (slot.valid_until < today) return 'slot-past';
    if (slot.valid_from > today) return 'slot-future';
    return 'slot-active';
}

const previewStyle = computed(() => {
    const start = Math.min(draw.startMin, draw.endMin) - DAY_START_H * 60;
    const end = Math.max(draw.startMin, draw.endMin) - DAY_START_H * 60;
    return {
        top: `${minuteToPercent(start)}%`,
        height: `${minuteToPercent(end - start)}%`,
    };
});

function onSlotSave(slot: Partial<TimeSlot>) {
    if (slot.id) {
        emit('update', slot);
    } else {
        emit('create', slot);
    }
}

function onSlotDelete(slotId: number) {
    emit('delete', slotId);
}
</script>

<style scoped>
.slot-planner-wrapper {
    overflow-x: auto;
}

.slot-planner {
    display: flex;
    min-width: 700px;
    user-select: none;
}

.time-axis {
    width: 3.5rem;
    flex-shrink: 0;
}

.day-header-placeholder {
    height: 2rem;
}

.time-labels {
    position: relative;
    height: 600px;
}

.time-label {
    position: absolute;
    font-size: 0.65rem;
    color: var(--p-text-muted-color);
    transform: translateY(-50%);
    left: 0;
    right: 0;
    text-align: right;
    padding-right: 6px;
}

.days-area {
    display: flex;
    flex: 1;
    gap: 2px;
}

.day-col {
    flex: 1;
    min-width: 80px;
}

.day-header {
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--p-text-muted-color);
}

.timeline-area {
    position: relative;
    height: 600px;
    background: var(--p-content-background);
    border: 1px solid var(--p-content-border-color);
    border-radius: var(--p-border-radius-sm, 4px);
    cursor: crosshair;
    overflow: hidden;
}

.grid-line {
    position: absolute;
    left: 0;
    right: 0;
    height: 1px;
    background: var(--p-content-border-color);
    pointer-events: none;
}

.grid-line.half {
    background: var(--p-content-hover-background);
}

.slot-block {
    position: absolute;
    left: 2px;
    right: 2px;
    border-radius: 4px;
    padding: 2px 4px;
    font-size: 0.65rem;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
    transition: filter 0.15s;
    min-height: 20px;
}

.slot-block:hover {
    filter: brightness(0.9);
}

.slot-active {
    background: #7f24b4;
    color: white;
}

.slot-future {
    background: #a78bfa;
    color: white;
    opacity: 0.7;
}

.slot-past {
    background: #94a3b8;
    color: white;
    opacity: 0.5;
}

.slot-label {
    font-weight: 600;
    line-height: 1.2;
}

.slot-sub {
    opacity: 0.8;
    line-height: 1.1;
}

.slot-preview {
    position: absolute;
    left: 2px;
    right: 2px;
    background: rgba(127, 36, 180, 0.3);
    border: 2px dashed #7f24b4;
    border-radius: 4px;
    pointer-events: none;
}
</style>
