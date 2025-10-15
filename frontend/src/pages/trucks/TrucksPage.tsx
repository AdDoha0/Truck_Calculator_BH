import React, { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import TruckListSection from './sections/TruckListSection';
import TruckFormSection from './sections/TruckFormSection';
import TruckCostsTableSection from './sections/TruckCostsTableSection';
import CommonCostsSection from './sections/CommonCostsSection';
import TruckCard from '../../features/trucks/components/TruckCard';
import Button from '../../shared/ui/Button';
import Select from '../../shared/ui/Select';
import ConfirmDialog from '../../shared/ui/ConfirmDialog';
import { useApi, useApiMutation } from '../../shared/hooks/useApi';
import { trucksApi } from '../../features/trucks/api/trucksApi';
import { costsApi } from '../../features/costs/api/costsApi';
import { snapshotsApi } from '../../features/snapshots/api/snapshotsApi';
import type { Truck } from '../../types';

type ViewMode = 'cards' | 'table';

const TrucksPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [showForm, setShowForm] = useState(false);
  const [editingTruck, setEditingTruck] = useState<Truck | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>('cards');
  const [selectedMonth, setSelectedMonth] = useState<string>(() => {
    const periodFromUrl = searchParams.get('period');
    return periodFromUrl || new Date().toISOString().slice(0, 16);
  });
  const [deleteConfirm, setDeleteConfirm] = useState<{ isOpen: boolean; truck: Truck | null }>({
    isOpen: false,
    truck: null,
  });
  const [showSnapshotModal, setShowSnapshotModal] = useState(false);
  const [snapshotData, setSnapshotData] = useState({
    period_date: new Date().toISOString().slice(0, 10),
    label: ''
  });

  const { data: trucks, loading: trucksLoading, refetch: refetchTrucks } = useApi(trucksApi.getTrucks);
  
  // Получаем данные периода с снимком фиксированных затрат
  const { data: periodData, refetch: refetchPeriodData } = useApi(() => {
    // Если выбран "current", получаем текущие данные
    if (selectedMonth === 'current') {
      return costsApi.getCurrentData();
    }
    
    // Передаем идентификатор снимка
    return costsApi.getPeriodDataWithSnapshot({ snapshot_id: selectedMonth as any });
  }, [selectedMonth]);
  
  const { data: periods } = useApi(costsApi.getPeriods);
  const deleteMutation = useApiMutation(trucksApi.deleteTruck);
  const createSnapshotMutation = useApiMutation(snapshotsApi.createFromCurrentData);

  // Инициализируем выбранный период первым доступным из базы данных
  React.useEffect(() => {
    if (periods && periods.length > 0 && selectedMonth === new Date().toISOString().slice(0, 16)) {
      setSelectedMonth(periods[0].value);
    }
  }, [periods, selectedMonth]);

  const handleEdit = (truck: Truck) => {
    setEditingTruck(truck);
    setShowForm(true);
  };

  const handleDelete = (truck: Truck) => {
    setDeleteConfirm({ isOpen: true, truck });
  };

  const confirmDelete = async () => {
    if (!deleteConfirm.truck?.id) return;
    
    try {
      await deleteMutation.mutate(deleteConfirm.truck.id);
      setDeleteConfirm({ isOpen: false, truck: null });
      refetchTrucks();
    } catch (error) {
      console.error('Ошибка при удалении трака:', error);
    }
  };

  const handleCreateSnapshot = async () => {
    try {
      await createSnapshotMutation.mutate(snapshotData);
      setShowSnapshotModal(false);
      setSnapshotData({ period_date: new Date().toISOString().slice(0, 10), label: '' });
      // Обновляем данные и переключаемся на новый период
      refetchPeriodData();
      // Можно добавить уведомление об успехе
      alert('Снимок успешно создан!');
    } catch (error) {
      console.error('Error creating snapshot:', error);
      alert('Ошибка при создании снимка');
    }
  };

  const handleFormSubmit = () => {
    setShowForm(false);
    setEditingTruck(null);
    refetchTrucks();
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingTruck(null);
  };

  const handleViewDetails = (truck: Truck) => {
    navigate(`/trucks/${truck.id}?period=${encodeURIComponent(selectedMonth)}`);
  };

  // Объединяем данные траков с затратами
  const trucksWithCosts = trucks?.map(truck => {
    // Получаем фиксированные затраты из снимка
    const truckFixedCosts = periodData?.fixed_costs?.trucks?.find((tc: any) => tc.truck_id === truck.id);
    // Получаем переменные затраты за период
    const truckVariableCosts = periodData?.variable_costs?.find((vc: any) => vc.truck === truck.id);
    return {
      ...truck,
      fixed_costs: truckFixedCosts,
      latest_variable_costs: truckVariableCosts,
    };
  }) || [];

  const monthOptions = React.useMemo(() => {
    // Если есть периоды из базы данных, используем их
    if (periods && periods.length > 0) {
      return periods.map(period => ({
        value: period.value,
        label: period.label
      }));
    }
    
    // Fallback: генерируем месяцы как раньше
    const months = [];
    const now = new Date();
    for (let i = 0; i < 12; i++) {
      const date = new Date(now.getFullYear(), now.getMonth() - i, 1);
      const value = date.toISOString().slice(0, 7);
      const label = date.toLocaleDateString('ru-RU', { year: 'numeric', month: 'long' });
      months.push({ value, label });
    }
    return months;
  }, [periods]);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-start gap-6">
        <div className="flex-1">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h1 className="text-3xl font-bold text-secondary-900">Траки</h1>
              <p className="text-secondary-600 mt-1">
                Управление траками и их данными
              </p>
              {periodData?.snapshot ? (
                <div className="mt-2 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                  <p className="text-sm text-blue-800">
                    <span className="font-medium">Снимок фиксированных затрат:</span> {periodData.snapshot.label || 'Автоматический снимок'} 
                    <span className="text-blue-600 ml-2">
                      (создан: {new Date(periodData.snapshot.snapshot_at).toLocaleString('ru-RU')})
                    </span>
                  </p>
                </div>
              ) : selectedMonth === 'current' ? (
                <div className="mt-2 p-3 bg-green-50 border border-green-200 rounded-lg">
                  <p className="text-sm text-green-800">
                    <span className="font-medium">Текущие данные:</span> Отображаются актуальные фиксированные затраты на данный момент
                  </p>
                </div>
              ) : null}
              
              {selectedMonth === 'current' && (
                <div className="mt-3">
                  <Button
                    onClick={() => setShowSnapshotModal(true)}
                    variant="primary"
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    📸 Сохранить период
                  </Button>
                </div>
              )}
            </div>
            <Button
              onClick={() => setShowForm(true)}
              variant="primary"
            >
              Добавить трак
            </Button>
          </div>

          {showForm && (
            <div className="mb-6">
              <TruckFormSection
                truck={editingTruck || undefined}
                onSubmit={handleFormSubmit}
                onCancel={handleFormCancel}
              />
            </div>
          )}

          <div className="flex justify-between items-center mb-4">
            <div className="flex items-center space-x-4">
              <div className="flex bg-secondary-100 rounded-lg p-1">
                <button
                  onClick={() => setViewMode('cards')}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    viewMode === 'cards'
                      ? 'bg-white text-secondary-900 shadow-sm'
                      : 'text-secondary-600 hover:text-secondary-900'
                  }`}
                >
                  Карточки
                </button>
                <button
                  onClick={() => setViewMode('table')}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    viewMode === 'table'
                      ? 'bg-white text-secondary-900 shadow-sm'
                      : 'text-secondary-600 hover:text-secondary-900'
                  }`}
                >
                  Таблица
                </button>
              </div>

              <Select
                label="Период"
                options={monthOptions}
                value={selectedMonth}
                onChange={(value) => {
                  // Если выбран период из базы данных, используем его полное значение
                  if (periods && periods.length > 0) {
                    const selectedPeriod = periods.find(p => p.value === value);
                    if (selectedPeriod) {
                      setSelectedMonth(selectedPeriod.value);
                      return;
                    }
                  }
                  // Fallback для сгенерированных месяцев
                  setSelectedMonth(value);
                }}
                className="w-48"
              />
            </div>
          </div>

          {viewMode === 'cards' ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {trucksLoading ? (
                <p>Загрузка...</p>
              ) : trucksWithCosts.length > 0 ? (
                trucksWithCosts.map(truck => (
                  <TruckCard
                    key={truck.id}
                    truck={truck}
                    variableCosts={truck.latest_variable_costs}
                    fixedCosts={truck.fixed_costs}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                    onViewDetails={handleViewDetails}
                  />
                ))
              ) : (
                <p className="text-secondary-500 col-span-full text-center py-8">
                  Траки не найдены
                </p>
              )}
            </div>
          ) : (
            <TruckCostsTableSection
              trucks={trucksWithCosts}
              loading={trucksLoading}
              onEdit={handleEdit}
              onDelete={handleDelete}
              onViewDetails={handleViewDetails}
            />
          )}
        </div>

        <div className="w-80">
          <CommonCostsSection 
            snapshotCommonCosts={periodData?.common_costs}
            isFromSnapshot={!!periodData?.snapshot}
            snapshotId={periodData?.snapshot?.id}
          />
        </div>
      </div>

      {/* Модальное окно создания снимка */}
      {showSnapshotModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96 max-w-full mx-4">
            <h3 className="text-lg font-semibold mb-4">Создать снимок периода</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Дата периода
                </label>
                <input
                  type="date"
                  value={snapshotData.period_date}
                  onChange={(e) => setSnapshotData(prev => ({ ...prev, period_date: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Метка (необязательно)
                </label>
                <input
                  type="text"
                  value={snapshotData.label}
                  onChange={(e) => setSnapshotData(prev => ({ ...prev, label: e.target.value }))}
                  placeholder="Например: Январь 2024"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div className="text-sm text-gray-600">
                <p className="font-medium mb-1">Будет сохранено:</p>
                <ul className="list-disc list-inside space-y-1">
                  <li>Фиксированные затраты (общие)</li>
                  <li>Фиксированные затраты по тракам</li>
                  <li>Переменные затраты по тракам</li>
                </ul>
              </div>
            </div>
            
            <div className="flex justify-end space-x-3 mt-6">
              <Button
                onClick={() => setShowSnapshotModal(false)}
                variant="secondary"
                disabled={createSnapshotMutation.loading}
              >
                Отмена
              </Button>
              <Button
                onClick={handleCreateSnapshot}
                variant="primary"
                loading={createSnapshotMutation.loading}
                className="bg-blue-600 hover:bg-blue-700"
              >
                Создать снимок
              </Button>
            </div>
          </div>
        </div>
      )}

      <ConfirmDialog
        isOpen={deleteConfirm.isOpen}
        title="Удалить трак?"
        message={`Вы уверены, что хотите удалить трак ${deleteConfirm.truck?.tractor_no}? Все связанные затраты будут также удалены.`}
        confirmText="Удалить"
        cancelText="Отмена"
        onConfirm={confirmDelete}
        onCancel={() => setDeleteConfirm({ isOpen: false, truck: null })}
        loading={deleteMutation.loading}
        variant="danger"
      />
    </div>
  );
};

export default TrucksPage;

