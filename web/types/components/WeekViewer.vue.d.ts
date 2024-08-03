import type { ShopWithOpenRange } from '@/api/types';
declare const _default: import("vue").DefineComponent<{
    shopId: {
        type: NumberConstructor;
        required: true;
    };
    year: {
        type: NumberConstructor;
        required: true;
    };
    weekNumber: {
        type: NumberConstructor;
        required: true;
    };
}, {}, {
    shopData: ShopWithOpenRange | null;
    dayBounds: {
        start_time: number;
        end_time: number;
    };
}, {}, {
    fetchShop(shopId: number): Promise<void>;
}, import("vue").ComponentOptionsMixin, import("vue").ComponentOptionsMixin, {}, string, import("vue").PublicProps, Readonly<import("vue").ExtractPropTypes<{
    shopId: {
        type: NumberConstructor;
        required: true;
    };
    year: {
        type: NumberConstructor;
        required: true;
    };
    weekNumber: {
        type: NumberConstructor;
        required: true;
    };
}>>, {}, {}>;
export default _default;
