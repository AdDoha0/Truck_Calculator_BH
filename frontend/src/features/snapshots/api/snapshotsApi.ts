import apiClient from '../../../services/api';
import type { CostSnapshot, CostSnapshotCreate } from '../../../types';

export const snapshotsApi = {
  // Получить все снимки
  getSnapshots: async (): Promise<CostSnapshot[]> => {
    const response = await apiClient.get('/snapshots/');
    return response.data;
  },

  // Получить снимок по ID
  getSnapshot: async (id: number): Promise<CostSnapshot> => {
    const response = await apiClient.get(`/snapshots/${id}/`);
    return response.data;
  },

  // Получить снимок по периоду
  getSnapshotByPeriod: async (periodDate: string): Promise<CostSnapshot | null> => {
    const response = await apiClient.get(`/snapshots/by_period/?period_date=${periodDate}`);
    return response.data;
  },

  // Получить детали снимка
  getSnapshotDetails: async (snapshotId: number, truckId?: number) => {
    const params = truckId ? `?truck_id=${truckId}` : '';
    const response = await apiClient.get(`/snapshots/${snapshotId}/details/${params}`);
    return response.data;
  },

  // Создать снимок
  createSnapshot: async (data: CostSnapshotCreate): Promise<CostSnapshot> => {
    const response = await apiClient.post('/snapshots/', data);
    return response.data;
  },

  // Восстановить из снимка
  restoreFromSnapshot: async (snapshotId: number): Promise<void> => {
    await apiClient.post(`/snapshots/${snapshotId}/restore/`);
  },

  // Удалить снимок
  deleteSnapshot: async (snapshotId: number): Promise<void> => {
    await apiClient.delete(`/snapshots/${snapshotId}/`);
  },

  // Сравнить снимки
  compareSnapshots: async (snapshotIds: number[]) => {
    const response = await apiClient.post('/snapshots/compare/', { snapshot_ids: snapshotIds });
    return response.data;
  },

  // Создать снимок из текущих данных
  createFromCurrentData: async (data: { period_date: string; label?: string }): Promise<CostSnapshot> => {
    const response = await apiClient.post('/snapshots/create_from_current_data/', data);
    return response.data;
  },
};

