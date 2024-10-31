type TokenResponse = {
    id: number,
    user_id: number,
    access_token: string,
    expires_at: Date,
    token_type: string
}


type User = {
    id: number,
    email: string,
    full_name: string,
    admin: boolean,
    group: string
    confirmed: boolean
}


const exampleUser: User = {
    id: -1,
    email: "Loading ...",
    full_name: "Loading ...",
    admin: false,
    group: "Loading ...",
    confirmed: false
}

type Shop = {
    id: number,
    name: string,
    description: string,
    location: string,
    maps_link: string
    volunteers: number,
    min_time: number,
    max_time: number,
    available_from: string,
    available_until: string
}

type OpenRange = {
    id: number,
    day: number,
    start_time: string,
    end_time: string
}

type ShopWithOpenRange = Shop & {
    open_ranges: OpenRange[]
}

type ReservedTimeRange = {
    id: number,
    start_time: string,
    duration_minutes: number,
    status: number,
    validated: boolean,
    title: string,
    shop: Shop | null
}
const exampleShop: Shop = {
    id: -1,
    name: "",
    description: "",
    location: "",
    maps_link: "https://maps.app.goo.gl/...",
    volunteers: 0,
    min_time: 0,
    max_time: 0,
    available_from: "0000-00-00",
    available_until: "0000-00-00"
}

const exampleReservedTimeRange: ReservedTimeRange = {
    id: -1,
    start_time: "1234-56-78 12:00",
    duration_minutes: 90,
    status: -1,
    validated: false,
    title: "Loading ...",
    shop: exampleShop
}

const exampleOpenRange: OpenRange = {
    id: -1,
    day: 0,
    start_time: "00:00",
    end_time: "00:00"
}

const exampleShopWithOpenRange: ShopWithOpenRange = {
    ...exampleShop,
    open_ranges: [exampleOpenRange]
}

type BookRangeRequest = {
    start_time: string,
    duration_minutes: number
}
type Setting = {
    key: string,
    value: string,
    private: boolean
}

type Notification = {
    id: number,
    user_id: number | null,
    message: string
    date: string
    data: string,
    icon: string | null,
    is_reminder: boolean,
    read: boolean,
    route: string | null,

    mail: boolean,
    mail_sent: boolean,
}

const exampleNotification: Notification = {
    id: -1,
    user_id: null,
    message: "notification.loading",
    date: "0000-00-00 00:00",
    data: "{}",
    is_reminder: false,
    read: true,
    icon: "pi pi-info-circle",
    route: "/notifications",

    mail: false,
    mail_sent: false,
}



export type { TokenResponse, User, Shop, OpenRange, ShopWithOpenRange, ReservedTimeRange, BookRangeRequest, Setting, Notification }
export { exampleShop, exampleReservedTimeRange, exampleOpenRange, exampleShopWithOpenRange, exampleUser, exampleNotification }