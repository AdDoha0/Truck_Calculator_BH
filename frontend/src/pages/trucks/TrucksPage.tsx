import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
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
import type { Truck } from '../../types';

type ViewMode = 'cards' | 'table';

const TrucksPage: React.FC = () => {
  const navigate = useNavigate();
  const [showForm, setShowForm] = useState(false);
  const [editingTruck, setEditingTruck] = useState<Truck | null>(null);
  const [viewMode, setViewMode] = useState<ViewMode>('cards');
  const [selectedMonth, setSelectedMonth] = useState<string>(new Date().toISOString().slice(0, 7));
  const [deleteConfirm, setDeleteConfirm] = useState<{ isOpen: boolean; truck: Truck | null }>({
    isOpen: false,
    truck: null,
  });

  const { data: trucks, loading: trucksLoading, refetch: refetchTrucks } = useApi(trucksApi.getTrucks);
  const { data: fixedCosts } = useApi(costsApi.getTruckFixedCosts);
  const { data: variableCosts } = useApi(() => costsApi.getVariableCosts({ period_month: selectedMonth }));
  const deleteMutation = useApiMutation(trucksApi.deleteTruck);

  const handleEdit = (truck: Truck) => {
    setEditingTruck(truck);
    setShowForm(true);
  };

  const handleDelete = (truck: Truck) => {
    setDeleteConfirm({ isOpen: true, truck });
  };

  const confirmDelete = async () => {
    if (!deleteConfirm.truck) return;
    
    try {
      await deleteMutation.mutate(deleteConfirm.truck.id);
      setDeleteConfirm({ isOpen: false, truck: null });
      refetchTrucks();
    } catch (error) {
      console.error('Ошибка при удалении трака:', error);
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
    navigate(`/trucks/${truck.id}`);
  };

  // Объединяем данные траков с затратами
  const trucksWithCosts = trucks?.map(truck => {
    const truckFixedCosts = fixedCosts?.find(fc => fc.truck === truck.id);
    const truckVariableCosts = variableCosts?.find(vc => vc.truck === truck.id);
    return {
      ...truck,
      fixed_costs: truckFixedCosts,
      latest_variable_costs: truckVariableCosts,
    };
  }) || [];

  const monthOptions = React.useMemo(() => {
    const months = [];
    const now = new Date();
    for (let i = 0; i < 12; i++) {
      const date = new Date(now.getFullYear(), now.getMonth() - i, 1);
      const value = date.toISOString().slice(0, 7);
      const label = date.toLocaleDateString('ru-RU', { year: 'numeric', month: 'long' });
      months.push({ value, label });
    }
    return months;
  }, []);

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
                onChange={(value) => setSelectedMonth(value)}
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
          <CommonCostsSection />
        </div>
      </div>

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

