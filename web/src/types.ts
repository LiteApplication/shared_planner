type Task = {
    start_time: number,
    end_time: number,
    color: string,
    title: string | null,
    description: string,
    id: number | null,
    _row: undefined | number,
    cursor: string,
    status: number | null | undefined, // -1 someone; -2 me; > 0 someone with id; -3 system
    // Slot-specific optional fields
    slot_id?: number,
    reservation_id?: number | null,
    remaining?: number,
    slot_date?: string,
    selected?: boolean,
}

export type { Task };
