import { api } from ".";
import type { Notification } from "./types";

export default class NotificationsApi {


    async count(): Promise<number> {
        const result = await api.get('/notifications/count');
        return result.data;
    }

    async list(): Promise<Notification[]> {
        const result = await api.get(`/notifications/list`);
        return result.data;
    }

    async list_unread(): Promise<Notification[]> {
        const result = await api.get(`/notifications/unread`);
        return result.data;
    }

    async delete(id: number): Promise<void> {
        await api.delete(`/notifications/id/${id}`);
    }

    async delete_all(): Promise<void> {
        await api.delete(`/notifications/all`);
    }

    async mark_as_read(id: number): Promise<Notification> {
        const result = await api.patch(`/notifications/id/${id}/read`);
        return result.data;
    }

    async mark_all_as_read(): Promise<Notification[]> {
        const result = await api.patch(`/notifications/all/read`);
        return result.data;
    }

    async mark_as_unread(id: number): Promise<Notification> {
        const result = await api.patch(`/notifications/id/${id}/unread`);
        return result.data;
    }

}

