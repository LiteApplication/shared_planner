import { type PropType } from 'vue';
import { type Task } from '../types';
declare const _default: import("vue").DefineComponent<{
    title: {
        type: StringConstructor;
        required: true;
    };
    startOfDay: {
        type: NumberConstructor;
        required: true;
    };
    endOfDay: {
        type: NumberConstructor;
        required: true;
    };
    tasks: {
        type: PropType<Task[]>;
        required: true;
        validator: (tasks: Task[]) => boolean;
    };
}, unknown, unknown, {
    timeIntervals(): {
        time: string;
        showLabel: boolean;
        label: string;
    }[];
    cssVars(): {
        '--subdivisions': number;
    };
    sortedTasksWithRows(): Task[];
}, {
    formatTime(time: string): string;
    taskStyle(task: Task): {
        top: string;
        height: string;
        backgroundColor: string;
        marginLeft: string;
    };
}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {}, string, import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    title: {
        type: StringConstructor;
        required: true;
    };
    startOfDay: {
        type: NumberConstructor;
        required: true;
    };
    endOfDay: {
        type: NumberConstructor;
        required: true;
    };
    tasks: {
        type: PropType<Task[]>;
        required: true;
        validator: (tasks: Task[]) => boolean;
    };
}>>, {}, {}>;
export default _default;
