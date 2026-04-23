import { api } from ".";
import type { BookSlotRequest, BookMultipleSlotsRequest, ReservedTimeRange, SlotStatus } from "./types";

export default class ReservationApi {
    async getPlanning(shopId: number, monday: string): Promise<SlotStatus[][]> {
        const result = await api.get(`/res/${shopId}/${monday}/list`);
        return result.data;
    }

    async bookSlot(shopId: number, req: BookSlotRequest): Promise<ReservedTimeRange> {
        const result = await api.post(`/res/${shopId}/book`, req);
        return result.data;
    }

    async bookSlots(shopId: number, req: BookMultipleSlotsRequest): Promise<ReservedTimeRange> {
        const result = await api.post(`/res/${shopId}/book_multiple`, req);
        return result.data;
    }

    async cancel(reservationId: number): Promise<void> {
        await api.delete(`/res/${reservationId}/cancel`);
    }

    async validate(reservationId: number): Promise<void> {
        await api.put(`/res/${reservationId}/validate`);
    }

    async reassign(reservationId: number, userId: number): Promise<void> {
        await api.put(`/res/${reservationId}/reassign`, userId);
    }

    async getReservations(userId: number): Promise<ReservedTimeRange[]> {
        const result = await api.get(`/res/${userId}/list_user`);
        return result.data;
    }

    async myReservations(): Promise<ReservedTimeRange[]> {
        const result = await api.get(`/res/list_self_future`);
        return result.data;
    }

    async search(search: { shop_id: number | undefined, monday: string | undefined, user_id: number | undefined }): Promise<ReservedTimeRange[]> {
        const result = await api.post(`/res/search`, search);
        return result.data;
    }
}
