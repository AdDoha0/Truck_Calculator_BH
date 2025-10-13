import React, { useState } from 'react';
import Card from '../../../shared/ui/Card';
import Button from '../../../shared/ui/Button';
import Modal from '../../../shared/ui/Modal';
import TruckForm from '../../../features/trucks/components/TruckForm';
import { useApiMutation } from '../../../shared/hooks/useApi';
import { trucksApi } from '../../../features/trucks/api/trucksApi';
import type { Truck, TruckCreate } from '../../../types';

interface TruckInfoSectionProps {
  truck: Truck;
  onUpdate: () => void;
}

const TruckInfoSection: React.FC<TruckInfoSectionProps> = ({ truck, onUpdate }) => {
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const updateMutation = useApiMutation((params: { id: number; data: TruckCreate }) => 
    trucksApi.updateTruck(params.id, params.data)
  );

  const handleSubmit = async (data: TruckCreate) => {
    try {
      await updateMutation.mutate({ id: truck.id, data });
      setIsEditModalOpen(false);
      onUpdate();
    } catch (error) {
      console.error('Ошибка при обновлении трака:', error);
    }
  };

  return (
    <>
      <Card title="Информация о траке">
        <div className="space-y-4">
          <div>
            <p className="text-sm text-secondary-600">Номер трактора</p>
            <p className="text-lg font-semibold text-secondary-900">{truck.tractor_no}</p>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-secondary-600">Дата создания</p>
              <p className="text-secondary-900">
                {new Date(truck.created_at).toLocaleDateString('ru-RU')}
              </p>
            </div>
            <div>
              <p className="text-sm text-secondary-600">Последнее обновление</p>
              <p className="text-secondary-900">
                {new Date(truck.updated_at).toLocaleDateString('ru-RU')}
              </p>
            </div>
          </div>

          <div className="pt-2">
            <Button
              variant="secondary"
              size="sm"
              onClick={() => setIsEditModalOpen(true)}
            >
              Редактировать
            </Button>
          </div>
        </div>
      </Card>

      <Modal
        isOpen={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        title="Редактировать трак"
      >
        <TruckForm
          truck={truck}
          onSubmit={handleSubmit}
          onCancel={() => setIsEditModalOpen(false)}
          loading={updateMutation.loading}
        />
      </Modal>
    </>
  );
};

export default TruckInfoSection;

