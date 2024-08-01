import { api } from ".";
import type { OpenRange, Shop, ShopWithOpenRange } from "./types";

export default class ShopApi {
    async get(id: number): Promise<ShopWithOpenRange> {
        const result = await api.get(`/shops/get/${id}`);
        return result.data;
    }

    async list(): Promise<Shop[]> {
        const result = await api.get("/shops/list");
        return result.data;
    }

    async create(shop: Shop): Promise<ShopWithOpenRange> {
        const result = await api.post("/shops/create", shop);
        return result.data;
    }

    async update(shop: ShopWithOpenRange): Promise<ShopWithOpenRange> {
        const result = await api.post("/shops/update/{shop.id}", shop);
        return result.data;
    }

    async delete(id: number): Promise<void> {
        const result = await api.post(`/shops/delete/${id}`);
        return result.data;
    }

    async addOpenRange(shopId: number, openRange: OpenRange): Promise<ShopWithOpenRange> {
        const result = await api.post(`/timeranges/create/${shopId}`, openRange);
        return result.data;
    }

    async deleteOpenRange(id: number): Promise<ShopWithOpenRange> {
        const result = await api.post(`/timeranges/delete/${id}`);
        return result.data;
    }

    async updateOpenRange(openRange: OpenRange): Promise<ShopWithOpenRange> {
        const result = await api.post(`/timeranges/update/${openRange.id}`, openRange);
        return result.data;
    }

}