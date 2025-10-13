import React from 'react';
import Table from '../../../shared/ui/Table';
import Button from '../../../shared/ui/Button';
import type { TableColumn } from '../../../shared/ui/types';
import type { Truck } from '../../../types';

interface TruckWithCosts extends Truck {
  fixed_costs?: {
    truck_payment: number;
    trailer_payment: number;
    physical_damage_insurance_truck: number;
    physical_damage_insurance_trailer: number;
  };
  latest_variable_costs?: {
    period_month: string;
    driver_name?: string;
    total_rev: number;
    total_miles: number;
    salary: number;
    fuel: number;
    tolls: number;
  };
}

interface TruckCostsTableSectionProps {
  trucks: TruckWithCosts[];
  loading?: boolean;
  onEdit: (truck: Truck) => void;
  onDelete: (truck: Truck) => void;
  onViewDetails: (truck: Truck) => void;
}

const TruckCostsTableSection: React.FC<TruckCostsTableSectionProps> = ({
  trucks,
  loading = false,
  onEdit,
  onDelete,
  onViewDetails,
}) => {
  const columns: TableColumn<TruckWithCosts>[] = [
    {
      key: 'tractor_no',
      title: 'Номер трака',
      sortable: true,
    },
    {
      key: 'fixed_costs',
      title: 'Платеж за трак',
      render: (_, truck) => truck.fixed_costs?.truck_payment ? `$${truck.fixed_costs.truck_payment}` : '-',
    },
    {
      key: 'fixed_costs',
      title: 'Платеж за прицеп',
      render: (_, truck) => truck.fixed_costs?.trailer_payment ? `$${truck.fixed_costs.trailer_payment}` : '-',
    },
    {
      key: 'latest_variable_costs',
      title: 'Период',
      render: (_, truck) => truck.latest_variable_costs?.period_month 
        ? (() => {
            try {
              // Если дата в формате YYYY-MM, добавляем день для корректного парсинга
              const dateValue = truck.latest_variable_costs.period_month.length === 7 
                ? `${truck.latest_variable_costs.period_month}-01` 
                : truck.latest_variable_costs.period_month;
              return new Date(dateValue).toLocaleDateString('ru-RU', { year: 'numeric', month: 'short' });
            } catch {
              return truck.latest_variable_costs.period_month;
            }
          })()
        : '-',
    },
    {
      key: 'latest_variable_costs',
      title: 'Водитель',
      render: (_, truck) => truck.latest_variable_costs?.driver_name || '-',
    },
    {
      key: 'latest_variable_costs',
      title: 'Выручка',
      render: (_, truck) => truck.latest_variable_costs?.total_rev ? `$${truck.latest_variable_costs.total_rev}` : '-',
    },
    {
      key: 'latest_variable_costs',
      title: 'Пробег',
      render: (_, truck) => truck.latest_variable_costs?.total_miles ? `${truck.latest_variable_costs.total_miles} mi` : '-',
    },
    {
      key: 'latest_variable_costs',
      title: 'Зарплата',
      render: (_, truck) => truck.latest_variable_costs?.salary ? `$${truck.latest_variable_costs.salary}` : '-',
    },
    {
      key: 'latest_variable_costs',
      title: 'Топливо',
      render: (_, truck) => truck.latest_variable_costs?.fuel ? `$${truck.latest_variable_costs.fuel}` : '-',
    },
    {
      key: 'actions',
      title: 'Действия',
      render: (_, truck) => (
        <div className="flex space-x-2">
          <Button
            size="sm"
            variant="primary"
            onClick={() => onViewDetails(truck)}
          >
            Детали
          </Button>
          <Button
            size="sm"
            variant="secondary"
            onClick={() => onEdit(truck)}
          >
            Ред.
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

export default TruckCostsTableSection;

