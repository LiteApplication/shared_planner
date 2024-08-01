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

/*
{
      "id": 0,
      "day": 0,
      "start_time": "09:33:16.570Z",
      "end_time": "09:33:16.570Z"
    }
      */
interface OpenRange {
    id: number,
    day: number,
    start_time: Date,
    end_time: Date
}

interface ShopWithOpenRange extends Shop {
    open_ranges: OpenRange[]
}


export type { TokenResponse, User, Shop, OpenRange, ShopWithOpenRange }