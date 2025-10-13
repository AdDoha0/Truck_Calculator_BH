import * as React from 'react';
import { useApi } from '../../../shared/hooks/useApi';
import { trucksApi } from '../../../features/trucks/api/trucksApi';
import TruckTable from '../../../features/trucks/components/TruckTable';
import Loader from '../../../shared/ui/Loader';

interface TruckListSectionProps {
  onEdit: (truck: any) => void;
  onDelete: (truck: any) => void;
}

const TruckListSection: React.FC<TruckListSectionProps> = ({
  onEdit,
  onDelete,
}) => {
  const { data: trucks, loading, error } = useApi(trucksApi.getTrucks);

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4">
        <p className="text-red-600">Ошибка загрузки траков: {error}</p>
      </div>
    );
  }

  return (
    <div>
      <TruckTable
        trucks={trucks || []}
        loading={loading}
        onEdit={onEdit}
        onDelete={onDelete}
      />
    </div>
  );
};

export default TruckListSection;

