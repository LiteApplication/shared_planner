import { api } from ".";
import type { TimeSlot } from "./types";

type TimeSlotIn = {
    day: number,
    start_time: string,
    end_time: string,
    max_volunteers: number,
    valid_from: string,
    valid_until: string
}

export default class SlotsApi {
    async list(shopId: number): Promise<TimeSlot[]> {
        const result = await api.get(`/slots/${shopId}/list`);
        return result.data;
    }

    async create(shopId: number, slot: TimeSlotIn): Promise<TimeSlot> {
        const result = await api.post(`/slots/${shopId}/create`, slot);
        return result.data;
    }

    async update(slotId: number, slot: TimeSlotIn): Promise<TimeSlot> {
        const result = await api.put(`/slots/${slotId}/update`, slot);
        return result.data;
    }

    async delete(slotId: number): Promise<void> {
        await api.delete(`/slots/${slotId}/delete`);
    }
}
