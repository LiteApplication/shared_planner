interface TokenResponse {
    id: number,
    user_id: number,
    access_token: string,
    expires_at: Date,
    token_type: string
}


interface User {
    id: number,
    email: string,
    full_name: string,
    admin: boolean,
}


interface Shop {
    id: number,
    name: string,
    description: string,
    location: string,
    latitude: number,
    longitude: number,
    volunteers: number,
    available_from: Date,
    available_until: Date
}

interface OpenRange {
    id: number,
    day: number,
    start_time: string,
    end_time: string
}

interface ShopWithOpenRange extends Shop {
    open_ranges: OpenRange[]
}


export type { TokenResponse, User, Shop, OpenRange, ShopWithOpenRange }