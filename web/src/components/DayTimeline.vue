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
            <div v-for="(task, index) in sortedTasksWithRows" class="task rounded" :key="index" :style="taskStyle(task)">
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

<script>
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'DayTimeline',
    components: {},
    props: {
        title: {
            type: String,
            required: true
        },
        startOfDay: {
            type: String,
            required: true
        },
        endOfDay: {
            type: String,
            required: true
        },
        tasks: {
            type: Array,
            required: true,
            validator: (tasks) =>
                tasks.every(
                    (task) =>
                        'start_time' in task &&
                        'end_time' in task &&
                        'color' in task &&
                        'tooltip' in task
                )
        },
    },
    computed: {
        timeIntervals() {
            const intervals = [];
            const startMinutes = this.timeToMinutes(this.startOfDay);
            const endMinutes = this.timeToMinutes(this.endOfDay);
            for (let i = startMinutes; i <= endMinutes; i += 30) {
                intervals.push({
                    time: this.minutesToTime(i),
                    showLabel: i % 60 === 0,
                    label: this.formatTime(this.minutesToTime(i))
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
            const sorted = [...this.tasks].sort((a, b) => this.timeToMinutes(a.start_time) - this.timeToMinutes(b.start_time));
            // Initialize an array to keep track of the end times of the rows
            let rows = [];

            // Iterate through the sorted tasks
            sorted.forEach((task) => {
                let assigned = false;

                // Try to assign the task to an existing row
                for (let i = 0; i < sorted.length; i++) {
                    if (task.start_time >= rows[i]) {
                        task.row = i;
                        rows[i] = task.end_time;
                        assigned = true;
                        break;
                    }
                }

                // If no existing row is available, create a new row
                if (!assigned) {
                    task.row = rows.length;
                    rows.push(task.end_time);
                }
            });
            return sorted;
        },

    },
    methods: {
        formatTime(time) {
            const [hour, minute] = time.split(':');
            return `${hour}:${minute}`;
        },
        taskStyle(task) {
            const totalMinutes =
                this.timeToMinutes(this.endOfDay) - this.timeToMinutes(this.startOfDay) + 30;
            const taskStart =
                this.timeToMinutes(task.start_time) - this.timeToMinutes(this.startOfDay) + 30;
            const taskEnd =
                this.timeToMinutes(task.end_time) - this.timeToMinutes(this.startOfDay) + 30;
            const topPercent = (taskStart / totalMinutes) * 100;
            const heightPercent = ((taskEnd - taskStart) / totalMinutes) * 100;

            const marginLeft = task.row;

            return {
                top: `${topPercent}%`,
                height: `${heightPercent}%`,
                backgroundColor: task.color,
                boxSizing: 'border-box',
                marginLeft: `${marginLeft}rem`


            };
        },
        timeToMinutes(time) {
            const [hour, minute] = time.split(':').map(Number);
            return hour * 60 + minute;
        },
        minutesToTime(minutes) {
            const hour = Math.floor(minutes / 60)
                .toString()
                .padStart(2, '0');
            const minute = (minutes % 60).toString().padStart(2, '0');
            return `${hour}:${minute}`;
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
    align-items: center;
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
}

.task .task-content {
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
</style>
