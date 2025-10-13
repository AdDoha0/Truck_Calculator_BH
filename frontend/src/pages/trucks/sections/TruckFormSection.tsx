import React from 'react';
import Card from '../../../shared/ui/Card';
import TruckForm from '../../../features/trucks/components/TruckForm';
import { useApiMutation } from '../../../shared/hooks/useApi';
import { trucksApi } from '../../../features/trucks/api/trucksApi';
import type { Truck, TruckCreate } from '../../../features/trucks/types';

interface TruckFormSectionProps {
  truck?: Truck;
  onSubmit: (data: TruckCreate) => void;
  onCancel: () => void;
}

const TruckFormSection: React.FC<TruckFormSectionProps> = ({
  truck,
  onSubmit,
  onCancel,
}) => {
  const createMutation = useApiMutation(trucksApi.createTruck);
  const updateMutation = useApiMutation(trucksApi.updateTruck);

  const handleSubmit = async (data: TruckCreate) => {
    try {
      if (truck) {
        await updateMutation.mutate({ id: truck.id, data });
      } else {
        await createMutation.mutate(data);
      }
      onSubmit(data);
    } catch (error) {
      console.error('Error saving truck:', error);
    }
  };

  const loading = createMutation.loading || updateMutation.loading;

  return (
    <Card title={truck ? 'Редактировать трак' : 'Добавить новый трак'}>
      <TruckForm
        truck={truck}
        onSubmit={handleSubmit}
        onCancel={onCancel}
        loading={loading}
      />
    </Card>
  );
};

export default TruckFormSection;
