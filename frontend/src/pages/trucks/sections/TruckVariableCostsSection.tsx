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

  const { data: variableCosts, loading, refetch } = useApi(() => costsApi.getVariableCosts({ truck_id: truckId }), [truckId]);
  const createMutation = useApiMutation(costsApi.createVariableCosts);
  const updateMutation = useApiMutation((params: { id: number; data: TruckVariableCostsCreate }) =>
    costsApi.updateVariableCosts(params.id, params.data)
  );
  const deleteMutation = useApiMutation(costsApi.deleteVariableCosts);

  const handleSubmit = async (data: TruckVariableCostsCreate) => {
    try {
      if (editingCosts?.id) {
        await updateMutation.mutate({ id: editingCosts.id, data });
      } else {
        // Проверяем, есть ли уже запись для этого трака и периода
        const existingRecord = variableCosts?.find(cost => {
          // Нормализуем даты для сравнения
          let existingDate = cost.period_month;
          let newDate = data.period_month;
          
          // Приводим к единому формату YYYY-MM-DDTHH:MM:SS
          if (existingDate.length === 7) {
            existingDate = `${existingDate}-01T00:00:00`;
          } else if (existingDate.length === 10) {
            existingDate = `${existingDate}T00:00:00`;
          } else if (existingDate.length === 16) {
            existingDate = `${existingDate}:00`;
          }
          
          if (newDate.length === 7) {
            newDate = `${newDate}-01T00:00:00`;
          } else if (newDate.length === 10) {
            newDate = `${newDate}T00:00:00`;
          } else if (newDate.length === 16) {
            newDate = `${newDate}:00`;
          }
          
          return cost.truck === data.truck && existingDate === newDate;
        });
        
        if (existingRecord) {
          alert(`Запись для трака и периода ${data.period_month} уже существует. Выберите другой период или отредактируйте существующую запись.`);
          return;
        }
        
        await createMutation.mutate(data);
      }
      setIsAddModalOpen(false);
      setEditingCosts(null);
      refetch();
    } catch (error) {
      console.error('Ошибка при сохранении переменных затрат:', error);
      // Показываем более подробную информацию об ошибке
      if (error.response?.data?.non_field_errors) {
        alert(`Ошибка валидации: ${error.response.data.non_field_errors.join(', ')}`);
      } else {
        alert('Произошла ошибка при сохранении данных');
      }
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
    if (!deleteConfirm.costs?.id) return;

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
      render: (value: string) => {
        try {
          // Обрабатываем различные форматы дат
          let dateValue = value;
          
          if (value.length === 7) {
            // YYYY-MM -> YYYY-MM-01T00:00:00
            dateValue = `${value}-01T00:00:00`;
          } else if (value.length === 10) {
            // YYYY-MM-DD -> YYYY-MM-DDTHH:MM:SS
            dateValue = `${value}T00:00:00`;
          } else if (value.length === 16) {
            // YYYY-MM-DDTHH:MM -> YYYY-MM-DDTHH:MM:SS
            dateValue = `${value}:00`;
          }
          
          const date = new Date(dateValue);
          return date.toLocaleString('ru-RU', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
          });
        } catch {
          return value;
        }
      },
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
        message={`Вы уверены, что хотите удалить данные за период ${deleteConfirm.costs?.period_month ? (() => {
          try {
            // Обрабатываем различные форматы дат
            let dateValue = deleteConfirm.costs.period_month;
            
            if (dateValue.length === 7) {
              dateValue = `${dateValue}-01T00:00:00`;
            } else if (dateValue.length === 10) {
              dateValue = `${dateValue}T00:00:00`;
            } else if (dateValue.length === 16) {
              dateValue = `${dateValue}:00`;
            }
            
            const date = new Date(dateValue);
            return date.toLocaleString('ru-RU', { 
              year: 'numeric', 
              month: 'long', 
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit'
            });
          } catch {
            return deleteConfirm.costs.period_month;
          }
        })() : ''}?`}
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

