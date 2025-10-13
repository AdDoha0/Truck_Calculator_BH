import React, { useState } from 'react';
import Card from '../../../shared/ui/Card';
import Button from '../../../shared/ui/Button';
import Modal from '../../../shared/ui/Modal';
import FixedCostsForm from '../../../features/costs/components/FixedCostsForm';
import { useApi, useApiMutation } from '../../../shared/hooks/useApi';
import { costsApi } from '../../../features/costs/api/costsApi';
import type { FixedCostsTruckCreate } from '../../../types';

interface TruckFixedCostsSectionProps {
  truckId: number;
}

const TruckFixedCostsSection: React.FC<TruckFixedCostsSectionProps> = ({ truckId }) => {
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const { data: fixedCosts, loading, refetch } = useApi(() => costsApi.getTruckFixedCostsByTruckId(truckId));
  const createMutation = useApiMutation(costsApi.createTruckFixedCosts);
  const updateMutation = useApiMutation((params: { id: number; data: FixedCostsTruckCreate }) =>
    costsApi.updateTruckFixedCosts(params.id, params.data)
  );

  const handleSubmit = async (data: FixedCostsTruckCreate) => {
    try {
      if (fixedCosts?.id) {
        await updateMutation.mutate({ id: fixedCosts.id, data });
      } else {
        await createMutation.mutate(data);
      }
      setIsEditModalOpen(false);
      refetch();
    } catch (error) {
      console.error('Ошибка при сохранении фиксированных затрат:', error);
    }
  };

  return (
    <>
      <Card title="Фиксированные затраты">
        <div className="space-y-3">
          {loading ? (
            <p className="text-secondary-500">Загрузка...</p>
          ) : fixedCosts ? (
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <span className="text-secondary-600">Платеж за трак:</span>
                <span className="ml-2 font-medium">${fixedCosts.truck_payment}</span>
              </div>
              <div>
                <span className="text-secondary-600">Платеж за прицеп:</span>
                <span className="ml-2 font-medium">${fixedCosts.trailer_payment}</span>
              </div>
              <div>
                <span className="text-secondary-600">Страхование трака:</span>
                <span className="ml-2 font-medium">${fixedCosts.physical_damage_insurance_truck}</span>
              </div>
              <div>
                <span className="text-secondary-600">Страхование прицепа:</span>
                <span className="ml-2 font-medium">${fixedCosts.physical_damage_insurance_trailer}</span>
              </div>
            </div>
          ) : (
            <p className="text-secondary-500">Нет данных о фиксированных затратах</p>
          )}

          <div className="pt-2">
            <Button
              variant="secondary"
              size="sm"
              onClick={() => setIsEditModalOpen(true)}
            >
              {fixedCosts ? 'Редактировать' : 'Добавить'}
            </Button>
          </div>
        </div>
      </Card>

      <Modal
        isOpen={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        title={fixedCosts ? 'Редактировать фиксированные затраты' : 'Добавить фиксированные затраты'}
      >
        <FixedCostsForm
          costs={fixedCosts || undefined}
          truckId={truckId}
          onSubmit={handleSubmit}
          onCancel={() => setIsEditModalOpen(false)}
          loading={createMutation.loading || updateMutation.loading}
        />
      </Modal>
    </>
  );
};

export default TruckFixedCostsSection;

