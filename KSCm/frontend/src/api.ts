import axios from 'axios';
import { apiUrl } from '@/env';
import {
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
  IStore,
  IStoreUpdate,
  IStoreCreate,
  IReportingFileCreate,
} from './interfaces';

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };
}


export const api = {
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);

    return axios.post(`${apiUrl}/api/v1/login/access-token`, params);
  },
  async getMe(token: string) {
    return axios.get<IUserProfile>(`${apiUrl}/api/v1/users/me`, authHeaders(token));
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return axios.put<IUserProfile>(`${apiUrl}/api/v1/users/me`, data, authHeaders(token));
  },
  async getUsers(token: string) {
    return axios.get<IUserProfile[]>(`${apiUrl}/api/v1/users/`, authHeaders(token));
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return axios.put(`${apiUrl}/api/v1/users/${userId}`, data, authHeaders(token));
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return axios.post(`${apiUrl}/api/v1/users/`, data, authHeaders(token));
  },
  async passwordRecovery(email: string) {
    return axios.post(`${apiUrl}/api/v1/password-recovery/${email}`);
  },
  async resetPassword(password: string, token: string) {
    return axios.post(`${apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token,
    });
  },
  async getStores(token: string) {
    return axios.get<IStore[]>(`${apiUrl}/api/v1/stores/`, authHeaders(token));
  },
  async updateStore(token: string, storeId: number, data: IStoreUpdate) {
    return axios.put(`${apiUrl}/api/v1/stores/${storeId}`, data, authHeaders(token));
  },
  async createStore(token: string, data: IStoreCreate) {
    return axios.post(`${apiUrl}/api/v1/stores/`, data, authHeaders(token));
  },
  async createReportingFile(token: string, data: IReportingFileCreate) {
    return axios.post(`${apiUrl}/api/v1/controlling/create`, data, authHeaders(token));
  },
  async getTickets(
      token: string, pageNumber: number = 0, itemsPerPage: number = 15, orderBy: string, desc: boolean = true,
  ) {
    return axios.get(`${apiUrl}/api/v1/tickets/`, {
      ...authHeaders(token),
      params: {page: pageNumber, size: itemsPerPage, order_by: orderBy, desc},
    });
  },
  async postFileObject(token: string, data: any, mediaType: string) {
    return axios.post(`${apiUrl}/api/v1/media/?media_type=${mediaType}`, data, authHeaders(token));
  },
  async createTask(token: string, mediaId: string) {
    return axios.get(`${apiUrl}/api/v1/media/${mediaId}`, { ...authHeaders(token), params: {task: 'True'}});
  },
  async getTaskStatus(token: string, taskId: string) {
   return axios.get(`${apiUrl}/api/v1/utils/task-status/`, { ...authHeaders(token), params: {task_id: taskId}});
  },
  async getClaims(
      token: string, pageNumber: number = 0, itemsPerPage: number = 15, orderBy: string, desc: boolean = true,
  ) {
    return axios.get(`${apiUrl}/api/v1/claims/`, {
      ...authHeaders(token),
      params: {page: pageNumber, size: itemsPerPage, order_by: orderBy, desc},
    });
  },
  async getStaticData(token: string) {
    return axios.get(`${apiUrl}/api/v1/controlling/static/`, authHeaders(token));
  },
};
