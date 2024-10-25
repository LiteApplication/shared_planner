import { api, cachedGet } from ".";
import type { Setting } from "./types";

export default class SettingsApi {


    async list(): Promise<Setting[]> {
        const result = await api.get('/settings/');
        return result.data;
    }

    async get(key: string): Promise<Setting> {
        return await cachedGet(`/settings/${key}`);
    }

    async update(key: string, value: string): Promise<Setting> {
        const result = await api.patch(`/settings/${key}`, value);
        return result.data;
    }
}

