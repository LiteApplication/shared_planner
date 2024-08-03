import type { AxiosInstance } from "axios";
import type { TokenResponse } from "./types";
declare const api: AxiosInstance;
declare function setToken(token: TokenResponse): void;
declare function forgetToken(): void;
export { api, setToken, forgetToken };
