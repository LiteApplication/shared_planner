interface Task {
    start_time: number;
    end_time: number;
    color: string;
    title: string | null;
    description: string;
    id: number | null;
    _row: undefined | number;
}
export type { Task };
