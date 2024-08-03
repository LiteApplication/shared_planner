declare const messages: {
    en: {
        message: {
            hello_world: string;
            login: string;
            register: string;
            email: string;
            password: string;
            full_name: string;
            group: string;
            logout: string;
            to_register: string;
            to_login: string;
            shop_open: string;
        };
        day: {
            0: string;
            1: string;
            2: string;
            3: string;
            4: string;
            5: string;
            6: string;
        };
        error: {
            unknown: string;
            fields: string;
            token: {
                invalid: string;
                expired: string;
            };
            admin: {
                required: string;
            };
            auth: {
                user_not_found: string;
                invalid_password: string;
                email_exists: string;
                password_too_short: string;
                full_name_too_short: string;
                email_invalid: string;
            };
            shop: {
                not_found: string;
                invalid_week: string;
                negative_time_range: string;
                time_range_overlap: string;
                time_range_not_found: string;
                id_mismatch: string;
            };
            reservation: {
                overlap: string;
                not_found: string;
                cant_cancel: string;
                cancel_validated: string;
            };
            user: {
                not_found: string;
                email_not_same: string;
                cant_set_self_admin: string;
            };
        };
    };
    fr: {
        message: {
            hello_world: string;
            login: string;
            register: string;
            email: string;
            password: string;
            full_name: string;
            group: string;
            logout: string;
            to_register: string;
            to_login: string;
            shop_open: string;
        };
        day: {
            0: string;
            1: string;
            2: string;
            3: string;
            4: string;
            5: string;
            6: string;
        };
        error: {
            unknown: string;
            fields: string;
            token: {
                invalid: string;
                expired: string;
            };
            admin: {
                required: string;
            };
            auth: {
                user_not_found: string;
                invalid_password: string;
                email_exists: string;
                password_too_short: string;
                full_name_too_short: string;
                email_invalid: string;
            };
            shop: {
                not_found: string;
                invalid_week: string;
                negative_time_range: string;
                time_range_overlap: string;
                time_range_not_found: string;
                id_mismatch: string;
            };
            reservation: {
                overlap: string;
                not_found: string;
                cant_cancel: string;
                cancel_validated: string;
            };
            user: {
                not_found: string;
                email_not_same: string;
                cant_set_self_admin: string;
            };
        };
    };
};
export default messages;
