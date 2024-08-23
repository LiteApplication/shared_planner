import { api } from ".";
import type { BookRangeRequest, ReservedTimeRange } from "./types";

export default class ReservationApi {
    async getPlanning(shopId: number, year: number, week: number): Promise<ReservedTimeRange[][]> {
        const result = await api.get(`/res/${shopId}/${year}/${week}/list`);
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


    async getReservations(userId: number): Promise<ReservedTimeRange[]> {
        const result = await api.get(`/res/${userId}/list_user`);
        return result.data;
    }
    async myReservations(): Promise<ReservedTimeRange[]> {
        const result = await api.get(`/res/list_self`);
        return result.data;
    }
}