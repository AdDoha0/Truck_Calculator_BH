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
import type { TruckCurrentVariableCosts } from '../../../types';

interface TruckVariableCostsSectionProps {
  truckId: number;
  selectedPeriod?: string;
}

const TruckVariableCostsSection: React.FC<TruckVariableCostsSectionProps> = ({ truckId, selectedPeriod }) => {
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [editingCosts, setEditingCosts] = useState<TruckCurrentVariableCosts | null>(null);
  const [deleteConfirm, setDeleteConfirm] = useState<{ isOpen: boolean; costs: TruckCurrentVariableCosts | null }>({
    isOpen: false,
    costs: null,
  });

  // Определяем, работаем ли с текущими данными или историческими
  const isCurrentData = selectedPeriod === 'current';

  // Получаем данные в зависимости от выбранного периода
  const currentDataHook = useApi(() => 
    costsApi.getCurrentVariableCostsByTruck(truckId), 
    [truckId, selectedPeriod]
  );
  
  const historicalDataHook = useApi(() => 
    costsApi.getVariableCosts({ truck_id: truckId, snapshot_id: selectedPeriod }), 
    [truckId, selectedPeriod]
  );
  
  const { data: variableCosts, loading, refetch } = isCurrentData ? currentDataHook : historicalDataHook;

  const createMutation = useApiMutation(
    isCurrentData ? costsApi.createCurrentVariableCosts : costsApi.createVariableCosts
  );
  const updateMutation = useApiMutation((params: { id: number; data: any }) =>
    isCurrentData 
      ? costsApi.updateCurrentVariableCosts(params.id, params.data)
      : costsApi.updateVariableCosts(params.id, params.data)
  );
  const deleteMutation = useApiMutation(
    isCurrentData ? costsApi.deleteCurrentVariableCosts : costsApi.deleteVariableCosts
  );

  const handleSubmit = async (data: any) => {
    try {
      if (editingCosts?.id) {
        await updateMutation.mutate({ id: editingCosts.id, data });
      } else {
        // Для текущих данных добавляем truck_id
        if (isCurrentData) {
          data.truck = truckId;
        }
        
        await createMutation.mutate(data);
      }
      setIsAddModalOpen(false);
      setEditingCosts(null);
      refetch();
    } catch (error: any) {
      console.error('Ошибка при сохранении переменных затрат:', error);
      // Показываем более подробную информацию об ошибке
      if (error.response?.data?.non_field_errors) {
        alert(`Ошибка валидации: ${error.response.data.non_field_errors.join(', ')}`);
      } else {
        alert('Произошла ошибка при сохранении данных');
      }
    }
  };

  const handleEdit = (costs: any) => {
    setEditingCosts(costs);
    setIsAddModalOpen(true);
  };

  const handleDelete = (costs: any) => {
    setDeleteConfirm({ isOpen: true, costs });
  };

  const confirmDelete = async () => {
    if (!deleteConfirm.costs?.id) return;

    try {
      await deleteMutation.mutate(deleteConfirm.costs.id);
      setDeleteConfirm({ isOpen: false, costs: null });
      refetch();
    } catch (error) {
      console.error('Ошибка при удалении переменных затрат:', error);
    }
  };

  const columns: TableColumn<any>[] = [
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
      render: (_: any, costs: any) => (
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

  // Преобразуем данные для отображения
  const displayData = isCurrentData 
    ? (variableCosts ? [variableCosts] : []) // Для текущих данных показываем одну запись
    : (Array.isArray(variableCosts) ? variableCosts : []); // Для исторических данных показываем массив

  return (
    <>
      <Card 
        title={isCurrentData ? "Текущие переменные затраты" : "Переменные затраты (снимок)"}
        actions={
          <Button
            variant="primary"
            size="sm"
            onClick={() => {
              setEditingCosts(null);
              setIsAddModalOpen(true);
            }}
          >
            {variableCosts ? 'Редактировать' : 'Добавить'}
          </Button>
        }
      >
        <Table
          data={displayData}
          columns={columns}
          loading={loading}
          emptyMessage={isCurrentData ? "Нет текущих переменных затрат" : "Нет данных о переменных затратах"}
        />
      </Card>

      <Modal
        isOpen={isAddModalOpen}
        onClose={() => {
          setIsAddModalOpen(false);
          setEditingCosts(null);
        }}
        title={editingCosts ? 'Редактировать переменные затраты' : (isCurrentData ? 'Добавить текущие переменные затраты' : 'Добавить переменные затраты')}
      >
        <VariableCostsForm
          costs={editingCosts as any || undefined}
          truckId={truckId}
          onSubmit={handleSubmit}
          onCancel={() => {
            setIsAddModalOpen(false);
            setEditingCosts(null);
          }}
          loading={createMutation.loading || updateMutation.loading}
          isCurrentData={isCurrentData}
        />
      </Modal>

      <ConfirmDialog
        isOpen={deleteConfirm.isOpen}
        title="Удалить переменные затраты?"
        message={isCurrentData ? "Вы уверены, что хотите удалить текущие переменные затраты?" : "Вы уверены, что хотите удалить запись прошлого периода?"}
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

