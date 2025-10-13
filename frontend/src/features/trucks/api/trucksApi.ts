import apiClient from '../../../services/api';
import type { Truck, TruckCreate } from '../../../types';

export const trucksApi = {
  // Получить все траки
  getTrucks: async (): Promise<Truck[]> => {
    const response = await apiClient.get('/trucks/');
    return response.data;
  },

  // Получить трак по ID
  getTruck: async (id: number): Promise<Truck> => {
    const response = await apiClient.get(`/trucks/${id}/`);
    return response.data;
  },

  // Создать новый трак
  createTruck: async (data: TruckCreate): Promise<Truck> => {
    const response = await apiClient.post('/trucks/', data);
    return response.data;
  },

  // Обновить трак
  updateTruck: async (id: number, data: Partial<TruckCreate>): Promise<Truck> => {
    const response = await apiClient.put(`/trucks/${id}/`, data);
    return response.data;
  },

  // Удалить трак
  deleteTruck: async (id: number): Promise<void> => {
    await apiClient.delete(`/trucks/${id}/`);
  },

  // Получить полную информацию о траке (с затратами)
  getTruckFullDetails: async (id: number): Promise<any> => {
    const response = await apiClient.get(`/trucks/${id}/full-details/`);
    return response.data;
  },
};
