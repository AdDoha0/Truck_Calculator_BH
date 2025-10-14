import apiClient from '../../../services/api';
import type { 
  FixedCostsCommon, 
  FixedCostsTruck, 
  FixedCostsTruckCreate,
  TruckVariableCosts, 
  TruckVariableCostsCreate 
} from '../../../types';

export const costsApi = {
  // Общие фиксированные затраты
  getCommonCosts: async (): Promise<FixedCostsCommon> => {
    const response = await apiClient.get('/costs/common/');
    return response.data;
  },

  updateCommonCosts: async (data: Partial<FixedCostsCommon>): Promise<FixedCostsCommon> => {
    const response = await apiClient.post('/costs/common/', data);
    return response.data;
  },

  // Фиксированные затраты трака
  getTruckFixedCosts: async (): Promise<FixedCostsTruck[]> => {
    const response = await apiClient.get('/costs/truck/');
    return response.data;
  },

  getTruckFixedCostsByTruckId: async (truckId: number): Promise<FixedCostsTruck | null> => {
    const response = await apiClient.get(`/costs/truck/by-truck/${truckId}/`);
    return response.data;
  },

  createTruckFixedCosts: async (data: FixedCostsTruckCreate): Promise<FixedCostsTruck> => {
    const response = await apiClient.post('/costs/truck/', data);
    return response.data;
  },

  updateTruckFixedCosts: async (id: number, data: Partial<FixedCostsTruckCreate>): Promise<FixedCostsTruck> => {
    const response = await apiClient.put(`/costs/truck/${id}/`, data);
    return response.data;
  },

  deleteTruckFixedCosts: async (id: number): Promise<void> => {
    await apiClient.delete(`/costs/truck/${id}/`);
  },

  // Переменные затраты трака
  getVariableCosts: async (params?: { 
    period_month?: string; 
    truck_id?: number 
  }): Promise<TruckVariableCosts[]> => {
    const response = await apiClient.get('/costs/variable/', { params });
    return response.data;
  },

  // Получить список периодов
  getPeriods: async (): Promise<Array<{
    value: string;
    label: string;
    date: string;
    datetime: string;
  }>> => {
    const response = await apiClient.get('/costs/variable/periods/');
    return response.data;
  },

  getVariableCost: async (id: number): Promise<TruckVariableCosts> => {
    const response = await apiClient.get(`/costs/variable/${id}/`);
    return response.data;
  },

  createVariableCosts: async (data: TruckVariableCostsCreate): Promise<TruckVariableCosts> => {
    const response = await apiClient.post('/costs/variable/', data);
    return response.data;
  },

  updateVariableCosts: async (id: number, data: Partial<TruckVariableCostsCreate>): Promise<TruckVariableCosts> => {
    const response = await apiClient.put(`/costs/variable/${id}/`, data);
    return response.data;
  },

  deleteVariableCosts: async (id: number): Promise<void> => {
    await apiClient.delete(`/costs/variable/${id}/`);
  },
};

