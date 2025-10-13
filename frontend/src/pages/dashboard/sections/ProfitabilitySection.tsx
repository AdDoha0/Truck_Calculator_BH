import * as React from 'react';
import Card from '../../../shared/ui/Card';
import Table from '../../../shared/ui/Table';
import type { TableColumn } from '../../../shared/ui/types';

// Временные данные для демонстрации
const mockData = [
  {
    id: 1,
    truck_tractor_no: 'TR-001',
    total_revenue: 245000,
    total_costs: 195000,
    profit: 50000,
    profit_margin: 20.4,
    profit_per_mile: 2.5,
  },
  {
    id: 2,
    truck_tractor_no: 'TR-002',
    total_revenue: 320000,
    total_costs: 240000,
    profit: 80000,
    profit_margin: 25.0,
    profit_per_mile: 3.2,
  },
  {
    id: 3,
    truck_tractor_no: 'TR-003',
    total_revenue: 180000,
    total_costs: 160000,
    profit: 20000,
    profit_margin: 11.1,
    profit_per_mile: 1.0,
  },
];

const ProfitabilitySection: React.FC = () => {
  const columns: TableColumn<typeof mockData[0]>[] = [
    {
      key: 'truck_tractor_no',
      title: 'Номер трака',
    },
    {
      key: 'total_revenue',
      title: 'Выручка',
      render: (value: number) => `₽${value.toLocaleString()}`,
    },
    {
      key: 'total_costs',
      title: 'Затраты',
      render: (value: number) => `₽${value.toLocaleString()}`,
    },
    {
      key: 'profit',
      title: 'Прибыль',
      render: (value: number) => (
        <span className={value >= 0 ? 'text-green-600' : 'text-red-600'}>
          ₽{value.toLocaleString()}
        </span>
      ),
    },
    {
      key: 'profit_margin',
      title: 'Маржа (%)',
      render: (value: number) => (
        <span className={value >= 20 ? 'text-green-600' : value >= 10 ? 'text-yellow-600' : 'text-red-600'}>
          {value.toFixed(1)}%
        </span>
      ),
    },
    {
      key: 'profit_per_mile',
      title: 'Прибыль/миля',
      render: (value: number) => `₽${value.toFixed(2)}`,
    },
  ];

  return (
    <Card title="Прибыльность по тракам">
      <Table
        data={mockData}
        columns={columns}
        emptyMessage="Нет данных о прибыльности"
      />
    </Card>
  );
};

export default ProfitabilitySection;
