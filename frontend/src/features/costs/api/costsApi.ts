import apiClient from '../../../services/api';
import type { 
  FixedCostsCommon, 
  FixedCostsTruck, 
  FixedCostsTruckCreate,
  TruckVariableCosts,
  TruckVariableCostsCreate,
  TruckCurrentVariableCosts,
  TruckCurrentVariableCostsCreate
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
    snapshot_id?: string | number; 
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

  // Получить данные периода с снимком фиксированных затрат
  getPeriodDataWithSnapshot: async (params: { 
    snapshot_id: string | number; 
  }): Promise<{
    variable_costs: TruckVariableCosts[];
    fixed_costs: any;
    common_costs: any;
    snapshot: any;
  }> => {
    const response = await apiClient.get('/costs/variable/by_period_with_snapshot/', { params });
    return response.data;
  },

  // Текущие переменные затраты
  getCurrentVariableCosts: async (params?: { 
    truck_id?: number 
  }): Promise<TruckCurrentVariableCosts[]> => {
    const response = await apiClient.get('/costs/current-variable/', { params });
    return response.data;
  },

  getCurrentVariableCost: async (id: number): Promise<TruckCurrentVariableCosts> => {
    const response = await apiClient.get(`/costs/current-variable/${id}/`);
    return response.data;
  },

  createCurrentVariableCosts: async (data: TruckCurrentVariableCostsCreate): Promise<TruckCurrentVariableCosts> => {
    const response = await apiClient.post('/costs/current-variable/', data);
    return response.data;
  },

  updateCurrentVariableCosts: async (id: number, data: Partial<TruckCurrentVariableCostsCreate>): Promise<TruckCurrentVariableCosts> => {
    const response = await apiClient.put(`/costs/current-variable/${id}/`, data);
    return response.data;
  },

  deleteCurrentVariableCosts: async (id: number): Promise<void> => {
    await apiClient.delete(`/costs/current-variable/${id}/`);
  },

  getCurrentVariableCostsByTruck: async (truckId: number): Promise<TruckCurrentVariableCosts> => {
    const response = await apiClient.get(`/costs/current-variable/by-truck/${truckId}/`);
    return response.data;
  },

  // Получить все текущие данные (фиксированные + переменные)
  getCurrentData: async (): Promise<{
    fixed_costs: {
      common: any;
      trucks: any[];
    };
    variable_costs: TruckCurrentVariableCosts[];
    common_costs: any;
    snapshot: null;
  }> => {
    const response = await apiClient.get('/costs/current-variable/current_data/');
    return response.data;
  },
};

