/**
 * API client for AvtoMat backend
 */
import axios from 'axios';
import type { City, School, Instructor, Application, ApplicationCreateData } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (window.location.protocol === 'https:' 
    ? 'https://194.110.54.230/api' 
    : 'http://localhost:8001/api');

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Cities
  getCities: async (): Promise<City[]> => {
    const response = await apiClient.get('/cities/');
    return response.data;
  },

  // Schools
  getSchools: async (city?: string): Promise<School[]> => {
    const params = city ? { city } : {};
    const response = await apiClient.get('/schools/', { params });
    return response.data;
  },

  // Instructors
  getInstructors: async (city?: string, autoType?: string): Promise<Instructor[]> => {
    const params: any = {};
    if (city) params.city = city;
    if (autoType) params.auto_type = autoType;
    const response = await apiClient.get('/instructors/', { params });
    return response.data;
  },

  // Applications
  createApplication: async (data: ApplicationCreateData): Promise<Application> => {
    const response = await apiClient.post('/applications/', data);
    return response.data;
  },

  getApplication: async (id: number): Promise<Application> => {
    const response = await apiClient.get(`/applications/${id}/`);
    return response.data;
  },

  // Telegram Auth
  telegramAuth: async (initData: string): Promise<any> => {
    const response = await apiClient.post('/auth/telegram/', { initData });
    return response.data;
  },
};

export default api;

