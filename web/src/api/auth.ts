import { api, forgetToken, setToken } from ".";
import type { User } from "./types";



export default class AuthApi {
  async login(email: string, password: string): Promise<void> {
    const bodyFormData = new FormData();
    bodyFormData.append('username', email);
    bodyFormData.append('password', password);
    const response = await api.post("/auth/login", bodyFormData);
    setToken(response.data);

  }

  async register(email: string, password: string, full_name: string, group: string): Promise<void> {
    const bodyFormData = new FormData();
    bodyFormData.append('email', email);
    bodyFormData.append('password', password);
    bodyFormData.append('full_name', full_name);
    bodyFormData.append('group', group);
    const response = await api.post("/auth/register", bodyFormData);
    setToken(response.data);
  }

  async me(): Promise<User> {
    return api.get("/auth/me").then(response => response.data);
  }

  async logout(): Promise<void> {
    try {
      forgetToken();
      await api.post("/auth/logout");
    } catch (e: any) {
      if (e.response?.status === 401) {
        return;
      }
      console.log(e)
    }
  }
}