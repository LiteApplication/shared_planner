import axios from "axios";
import type { AxiosInstance } from "axios";
import type { TokenResponse, User } from "./types";

const CACHE_TIMEOUT = 1000 * 60 * 1 / 60;

const api: AxiosInstance = axios.create({
    baseURL: "http://localhost:8000/api",
    headers: {
        "accept": "application/json",
    },
});

api.interceptors.request.use(
    config => {
        if (localStorage.getItem('access_token') !== null)
            config.headers['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`;
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);


function setToken(token: TokenResponse) {
    localStorage.setItem("access_token", token.access_token);
}

function forgetToken() {
    sessionStorage.removeItem('user');
    sessionStorage.removeItem('loginChecked');
    localStorage.removeItem("access_token");
}


function saveUserToSession(user: User) {
    sessionStorage.setItem('user', JSON.stringify(user));
    sessionStorage.setItem('loginChecked', Date.now().toString());
}

function loadUserFromSession(): User | null {
    if (Date.now() - parseInt(sessionStorage.getItem('loginChecked') || '0') > CACHE_TIMEOUT) {
        return null;
    }
    const user_data = sessionStorage.getItem('user');
    if (user_data) {
        return JSON.parse(user_data);
    }
    return null;
}

function cachedGet<T>(url: string): Promise<T> {
    const cached = sessionStorage.getItem("cache_data" + url);
    if (cached) {
        const cache_time = parseInt(sessionStorage.getItem("cache_time" + url) || '0');
        if (Date.now() - cache_time < CACHE_TIMEOUT) {
            return Promise.resolve(JSON.parse(cached));
        }
    }
    return api.get(url).then(response => {
        sessionStorage.setItem("cache_time" + url, Date.now().toString());
        sessionStorage.setItem("cache_data" + url, JSON.stringify(response.data));
        return response.data;
    });
}

function invalidateCache() {
    sessionStorage.clear();
}

export { api, setToken, forgetToken, saveUserToSession, loadUserFromSession, cachedGet, invalidateCache };