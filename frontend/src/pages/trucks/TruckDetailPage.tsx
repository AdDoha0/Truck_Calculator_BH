import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import Button from '../../shared/ui/Button';
import Loader from '../../shared/ui/Loader';
import ConfirmDialog from '../../shared/ui/ConfirmDialog';
import TruckInfoSection from './sections/TruckInfoSection';
import TruckFixedCostsSection from './sections/TruckFixedCostsSection';
import TruckVariableCostsSection from './sections/TruckVariableCostsSection';
import { useApi, useApiMutation } from '../../shared/hooks/useApi';
import { trucksApi } from '../../features/trucks/api/trucksApi';

const TruckDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [deleteConfirm, setDeleteConfirm] = useState(false);

  const truckId = parseInt(id || '0');
  const { data: truck, loading, refetch } = useApi(() => trucksApi.getTruck(truckId));
  const deleteMutation = useApiMutation(trucksApi.deleteTruck);

  const handleDelete = async () => {
    try {
      await deleteMutation.mutate(truckId);
      navigate('/trucks');
    } catch (error) {
      console.error('Ошибка при удалении трака:', error);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <Loader size="lg" />
      </div>
    );
  }

  if (!truck) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-600">Трак не найден</p>
        <Button variant="secondary" size="sm" onClick={() => navigate('/trucks')} className="mt-4">
          Вернуться к списку
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <div className="flex items-center space-x-3">
            <Button
              variant="secondary"
              size="sm"
              onClick={() => navigate('/trucks')}
            >
              ← Назад
            </Button>
            <h1 className="text-3xl font-bold text-secondary-900">
              Трак {truck?.tractor_no || 'Неизвестно'}
            </h1>
          </div>
          <p className="text-secondary-600 mt-1">
            Детальная информация и управление затратами
          </p>
        </div>
        <Button
          variant="danger"
          onClick={() => setDeleteConfirm(true)}
        >
          Удалить трак
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <TruckInfoSection truck={truck} onUpdate={refetch} />
        <TruckFixedCostsSection truckId={truckId} />
      </div>

      <TruckVariableCostsSection truckId={truckId} />

      <ConfirmDialog
        isOpen={deleteConfirm}
        title="Удалить трак?"
        message={`Вы уверены, что хотите удалить трак ${truck?.tractor_no || 'Неизвестно'}? Все связанные затраты будут также удалены. Это действие нельзя отменить.`}
        confirmText="Удалить"
        cancelText="Отмена"
        onConfirm={handleDelete}
        onCancel={() => setDeleteConfirm(false)}
        loading={deleteMutation.loading}
        variant="danger"
      />
    </div>
  );
};

export default TruckDetailPage;

