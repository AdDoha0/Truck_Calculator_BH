import React, { useState } from 'react';
import Card from '../../../shared/ui/Card';
import Button from '../../../shared/ui/Button';
import Modal from '../../../shared/ui/Modal';
import Table from '../../../shared/ui/Table';
import VariableCostsForm from '../../../features/costs/components/VariableCostsForm';
import ConfirmDialog from '../../../shared/ui/ConfirmDialog';
import { useApi, useApiMutation } from '../../../shared/hooks/useApi';
import { costsApi } from '../../../features/costs/api/costsApi';
import type { TableColumn } from '../../../shared/ui/types';
import type { TruckVariableCosts, TruckVariableCostsCreate } from '../../../types';

interface TruckVariableCostsSectionProps {
  truckId: number;
}

const TruckVariableCostsSection: React.FC<TruckVariableCostsSectionProps> = ({ truckId }) => {
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [editingCosts, setEditingCosts] = useState<TruckVariableCosts | null>(null);
  const [deleteConfirm, setDeleteConfirm] = useState<{ isOpen: boolean; costs: TruckVariableCosts | null }>({
    isOpen: false,
    costs: null,
  });

  const { data: variableCosts, loading, refetch } = useApi(() => costsApi.getVariableCosts({ truck_id: truckId }));
  const createMutation = useApiMutation(costsApi.createVariableCosts);
  const updateMutation = useApiMutation((params: { id: number; data: TruckVariableCostsCreate }) =>
    costsApi.updateVariableCosts(params.id, params.data)
  );
  const deleteMutation = useApiMutation(costsApi.deleteVariableCosts);

  const handleSubmit = async (data: TruckVariableCostsCreate) => {
    try {
      if (editingCosts) {
        await updateMutation.mutate({ id: editingCosts.id, data });
      } else {
        await createMutation.mutate(data);
      }
      setIsAddModalOpen(false);
      setEditingCosts(null);
      refetch();
    } catch (error) {
      console.error('Ошибка при сохранении переменных затрат:', error);
    }
  };

  const handleEdit = (costs: TruckVariableCosts) => {
    setEditingCosts(costs);
    setIsAddModalOpen(true);
  };

  const handleDelete = (costs: TruckVariableCosts) => {
    setDeleteConfirm({ isOpen: true, costs });
  };

  const confirmDelete = async () => {
    if (!deleteConfirm.costs) return;

    try {
      await deleteMutation.mutate(deleteConfirm.costs.id);
      setDeleteConfirm({ isOpen: false, costs: null });
      refetch();
    } catch (error) {
      console.error('Ошибка при удалении переменных затрат:', error);
    }
  };

  const columns: TableColumn<TruckVariableCosts>[] = [
    {
      key: 'period_month',
      title: 'Период',
      sortable: true,
      render: (value: string) => new Date(value).toLocaleDateString('ru-RU', { year: 'numeric', month: 'long' }),
    },
    {
      key: 'driver_name',
      title: 'Водитель',
      render: (value: string) => value || '-',
    },
    {
      key: 'total_rev',
      title: 'Выручка',
      render: (value: number) => `$${value}`,
    },
    {
      key: 'total_miles',
      title: 'Пробег',
      render: (value: number) => `${value} mi`,
    },
    {
      key: 'salary',
      title: 'Зарплата',
      render: (value: number) => `$${value}`,
    },
    {
      key: 'fuel',
      title: 'Топливо',
      render: (value: number) => `$${value}`,
    },
    {
      key: 'tolls',
      title: 'Дороги',
      render: (value: number) => `$${value}`,
    },
    {
      key: 'actions',
      title: 'Действия',
      render: (_, costs) => (
        <div className="flex space-x-2">
          <Button size="sm" variant="secondary" onClick={() => handleEdit(costs)}>
            Ред.
          </Button>
          <Button size="sm" variant="danger" onClick={() => handleDelete(costs)}>
            Удалить
          </Button>
        </div>
      ),
    },
  ];

  return (
    <>
      <Card 
        title="Переменные затраты по месяцам"
        actions={
          <Button
            variant="primary"
            size="sm"
            onClick={() => {
              setEditingCosts(null);
              setIsAddModalOpen(true);
            }}
          >
            Добавить
          </Button>
        }
      >
        <Table
          data={variableCosts || []}
          columns={columns}
          loading={loading}
          emptyMessage="Нет данных о переменных затратах"
        />
      </Card>

      <Modal
        isOpen={isAddModalOpen}
        onClose={() => {
          setIsAddModalOpen(false);
          setEditingCosts(null);
        }}
        title={editingCosts ? 'Редактировать переменные затраты' : 'Добавить переменные затраты'}
      >
        <VariableCostsForm
          costs={editingCosts || undefined}
          truckId={truckId}
          onSubmit={handleSubmit}
          onCancel={() => {
            setIsAddModalOpen(false);
            setEditingCosts(null);
          }}
          loading={createMutation.loading || updateMutation.loading}
        />
      </Modal>

      <ConfirmDialog
        isOpen={deleteConfirm.isOpen}
        title="Удалить переменные затраты?"
        message={`Вы уверены, что хотите удалить данные за период ${deleteConfirm.costs?.period_month ? new Date(deleteConfirm.costs.period_month).toLocaleDateString('ru-RU', { year: 'numeric', month: 'long' }) : ''}?`}
        confirmText="Удалить"
        cancelText="Отмена"
        onConfirm={confirmDelete}
        onCancel={() => setDeleteConfirm({ isOpen: false, costs: null })}
        loading={deleteMutation.loading}
        variant="danger"
      />
    </>
  );
};

export default TruckVariableCostsSection;

