<template>
    <div class="timeline rounded-lg border">
        <div class="timeline-header rounded-lg bg-slate-900">
            <p>{{ title }}</p>
        </div>
        <div class=" timeline-body divide-y divide-slate-500" :style="cssVars">
            <div v-for="(time, index) in timeIntervals" :key="index" class="time-line">
                <span v-if="time.showLabel" class="time-label text-slate-500">{{ time.label }}</span>
            </div>

        </div>
        <div class="timeline-container" :style="cssVars">
            <div v-for="(task, index) in sortedTasksWithRows" class="task rounded" :class="{ disabled: task.title == null }" :key="index"
                :style="taskStyle(task)" v-tooltip="(task.title == null) ? task.description : null">
                <div class="task-content">
                    <slot name="task" :task="task" v-if="task.title">
                        <h3>{{ task.title }}</h3>
                        <p>{{ task.description }}</p>
                    </slot>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import { timeToMinutes, minutesToTime } from '../utils';
import { type Task } from '../types';

export default defineComponent({
    name: 'DayTimeline',
    components: {},
    props: {
        title: {
            type: String,
            required: true
        },
        startOfDay: {
            type: Number,
            required: true
        },
        endOfDay: {
            type: Number,
            required: true
        },
        tasks: {
            type: Object as PropType<Task[]>,
            required: true,
            validator: (tasks: Task[]) =>
                tasks.every(
                    (task) =>
                        'start_time' in task &&
                        'end_time' in task &&
                        'color' in task &&
                        'title' in task &&
                        'description' in task
                )
        },
    },
    computed: {
        timeIntervals() {
            const intervals = [];
            for (let i = this.startOfDay; i <= this.endOfDay; i += 30) {
                intervals.push({
                    time: minutesToTime(i),
                    showLabel: i % 60 === 0,
                    label: this.formatTime(minutesToTime(i))
                });
            }
            return intervals;
        },
        cssVars() {
            return {
                '--subdivisions': this.timeIntervals.length
            };
        },
        sortedTasksWithRows() {
            const sorted: Task[] = [...this.tasks].sort((a, b) => a.start_time - b.start_time);
            // Initialize an array to keep track of the end times of the rows
            let rows: number[] = [];

            // Iterate through the sorted tasks
            sorted.forEach((task) => {
                let assigned = false;

                // Try to assign the task to an existing row
                for (let i = 0; i < sorted.length; i++) {
                    if (task.start_time >= rows[i]) {
                        task._row = i;
                        rows[i] = task.end_time;
                        assigned = true;
                        break;
                    }
                }

                // If no existing row is available, create a new row
                if (!assigned) {
                    task._row = rows.length;
                    rows.push(task.end_time);
                }
            });
            return sorted;
        },

    },
    methods: {
        formatTime(time: string) {
            const [hour, minute] = time.split(':');
            return `${hour}:${minute}`;
        },
        taskStyle(task: Task) {
            const totalMinutes =
                this.endOfDay - this.startOfDay + 30;
            const taskStart =
                task.start_time - this.startOfDay + 30;
            const taskEnd =
                task.end_time - this.startOfDay + 30;
            const topPercent = (taskStart / totalMinutes) * 100;
            const heightPercent = ((taskEnd - taskStart) / totalMinutes) * 100;

            const marginLeft = task._row;

            return {
                top: `${topPercent}%`,
                height: `${heightPercent}%`,
                backgroundColor: task.color,
                marginLeft: `${marginLeft}rem`
            };
        }
    }
});
</script>

<style scoped>
.timeline {
    width: 10rem;
    position: relative;
    margin: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s, width 0.3s;
}

.timeline:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    width: 30rem;
    z-index: 2;

}

.timeline-header {
    padding: 10px;
    text-align: center;
    font-weight: bold;
}

.timeline-body {
    position: absolute;
    overflow: hidden;
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: repeat(var(--subdivisions), calc(50rem / var(--subdivisions)));
    width: 100%;
    box-sizing: border-box;
}

.timeline-container {
    position: relative;
    height: 100%;
    width: 100%;
    box-sizing: border-box;
    height: 50rem;
}

.time-line {
    position: relative;
    display: flex;
    align-items: end;
    height: 100%;
}

.time-label {
    font: 0.8rem;
    padding-left: 0.5rem;
}

.task {
    position: absolute;
    left: calc(5 * 0.8rem);
    width: 1rem;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    z-index: 2;
    transition: width 0.3s;
    box-sizing: border-box;
}

.task .task-content {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;

    opacity: 0;
    transition: opacity 0.3 ease, width 0, height 0;
    width: 0;
    height: 0;
    color: white;
    padding: 0.5rem;
    z-index: -1;
    border-radius: 0.5rem;
}


.task .task-content h3 {
    font-weight: bold;
}

.task:hover .task-content {
    opacity: 1;
    z-index: 3;
    width: max-content;
    height: fit-content;
}

.task:hover {
    z-index: 3;
    width: 60%;
}

.task.disabled:hover {
    width: 1rem;
}
</style>
