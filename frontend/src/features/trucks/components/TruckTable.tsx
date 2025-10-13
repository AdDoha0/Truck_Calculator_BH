import * as React from 'react';
import Table from '../../../shared/ui/Table';
import Button from '../../../shared/ui/Button';
import type { Truck } from '../types';
import type { TableColumn } from '../../../shared/ui/types';

interface TruckTableProps {
  trucks: Truck[];
  loading?: boolean;
  onEdit: (truck: Truck) => void;
  onDelete: (truck: Truck) => void;
}

const TruckTable: React.FC<TruckTableProps> = ({
  trucks,
  loading = false,
  onEdit,
  onDelete,
}) => {
  const columns: TableColumn<Truck>[] = [
    {
      key: 'id',
      title: 'ID',
      sortable: true,
    },
    {
      key: 'tractor_no',
      title: 'Номер трактора',
      sortable: true,
    },
    {
      key: 'created_at',
      title: 'Дата создания',
      render: (value: string) => new Date(value).toLocaleDateString('ru-RU'),
    },
    {
      key: 'actions',
      title: 'Действия',
      render: (_, truck) => (
        <div className="flex space-x-2">
          <Button
            size="sm"
            variant="secondary"
            onClick={() => onEdit(truck)}
          >
            Редактировать
          </Button>
          <Button
            size="sm"
            variant="danger"
            onClick={() => onDelete(truck)}
          >
            Удалить
          </Button>
        </div>
      ),
    },
  ];

  return (
    <Table
      data={trucks}
      columns={columns}
      loading={loading}
      emptyMessage="Траки не найдены"
    />
  );
};

export default TruckTable;
