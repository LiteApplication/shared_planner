import { api } from ".";
import type { Setting } from "./types";

export default class SettingsApi {


    async list(): Promise<Setting[]> {
        const result = await api.get('/settings/');
        return result.data;
    }

    async get(key: string): Promise<Setting> {
        const result = await api.get(`/settings/${key}`);
        return result.data;
    }

    async update(key: string, value: string): Promise<Setting> {
        const result = await api.patch(`/settings/${key}`, value);
        return result.data;
    }
}

