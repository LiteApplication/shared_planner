import { api } from ".";
import type { BookRangeRequest, ReservedTimeRange } from "./types";

export default class ReservationApi {
    async getPlanning(shopId: number, monday: string): Promise<ReservedTimeRange[][]> {
        const result = await api.get(`/res/${shopId}/${monday}/list`);
        return result.data;
    }

    async reserve(shopId: number, range: BookRangeRequest): Promise<ReservedTimeRange> {
        const result = await api.post(`/res/${shopId}/book`, range);
        return result.data;
    }

    async update(reservationId: number, range: BookRangeRequest): Promise<ReservedTimeRange> {
        const result = await api.put(`/res/${reservationId}/update`, range);
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