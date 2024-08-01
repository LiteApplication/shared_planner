import axios from "axios";
import type { AxiosInstance } from "axios";
import type { TokenResponse } from "./types";


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
    localStorage.removeItem("access_token");
}


export { api, setToken, forgetToken };