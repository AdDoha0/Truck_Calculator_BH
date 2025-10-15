import React, { useState, useEffect } from 'react';
import Button from '../../../shared/ui/Button';
import Input from '../../../shared/ui/Input';
import type { TruckVariableCosts, TruckVariableCostsCreate, TruckCurrentVariableCosts, TruckCurrentVariableCostsCreate } from '../../../types';

interface VariableCostsFormProps {
  costs?: TruckVariableCosts | TruckCurrentVariableCosts;
  truckId: number;
  onSubmit: (data: TruckVariableCostsCreate | TruckCurrentVariableCostsCreate) => void;
  onCancel?: () => void;
  loading?: boolean;
  isCurrentData?: boolean;
}

const VariableCostsForm: React.FC<VariableCostsFormProps> = ({
  costs,
  truckId,
  onSubmit,
  onCancel,
  loading = false,
  isCurrentData = false,
}) => {
  const [formData, setFormData] = useState({
    period_month: new Date().toISOString().slice(0, 16), // YYYY-MM-DDTHH:MM
    driver_name: '',
    total_rev: '0',
    total_miles: '0',
    salary: '0',
    fuel: '0',
    tolls: '0',
  });

  useEffect(() => {
    if (costs) {
      // Для текущих данных не показываем поле period_month
      if (isCurrentData) {
        setFormData({
          period_month: '', // Не используется для текущих данных
          driver_name: costs.driver_name || '',
          total_rev: (costs.total_rev || 0).toString(),
          total_miles: (costs.total_miles || 0).toString(),
          salary: (costs.salary || 0).toString(),
          fuel: (costs.fuel || 0).toString(),
          tolls: (costs.tolls || 0).toString(),
        });
      } else {
        // Преобразуем дату в формат для datetime-local input
        let periodMonth = costs.period_month;
        
        // Если дата в формате YYYY-MM-DD, добавляем время
        if (periodMonth.length === 10) {
          periodMonth = `${periodMonth}T00:00`;
        }
        // Если дата в формате YYYY-MM, добавляем день и время
        else if (periodMonth.length === 7) {
          periodMonth = `${periodMonth}-01T00:00`;
        }
        // Если дата уже в формате YYYY-MM-DDTHH:MM:SS, обрезаем до YYYY-MM-DDTHH:MM
        else if (periodMonth.length === 19) {
          periodMonth = periodMonth.slice(0, 16);
        }
          
        setFormData({
          period_month: periodMonth,
          driver_name: costs.driver_name || '',
          total_rev: (costs.total_rev || 0).toString(),
          total_miles: (costs.total_miles || 0).toString(),
          salary: (costs.salary || 0).toString(),
          fuel: (costs.fuel || 0).toString(),
          tolls: (costs.tolls || 0).toString(),
        });
      }
    }
  }, [costs, isCurrentData]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (isCurrentData) {
      // Для текущих данных не включаем period_month
      const data: TruckCurrentVariableCostsCreate = {
        truck: truckId,
        driver_name: formData.driver_name || undefined,
        total_rev: parseFloat(formData.total_rev) || 0,
        total_miles: parseInt(formData.total_miles) || 0,
        salary: parseFloat(formData.salary) || 0,
        fuel: parseFloat(formData.fuel) || 0,
        tolls: parseFloat(formData.tolls) || 0,
      };
      
      console.log('Отправляемые данные (текущие):', data);
      onSubmit(data);
    } else {
      // Преобразуем YYYY-MM-DDTHH:MM в YYYY-MM-DDTHH:MM:SS для Django DateTimeField
      let periodMonth = formData.period_month;
      
      // Если время не указано, добавляем секунды
      if (periodMonth.length === 16) {
        periodMonth = `${periodMonth}:00`;
      }
      
      const data: TruckVariableCostsCreate = {
        period_month: periodMonth,
        truck: truckId,
        driver_name: formData.driver_name || undefined,
        total_rev: parseFloat(formData.total_rev) || 0,
        total_miles: parseInt(formData.total_miles) || 0,
        salary: parseFloat(formData.salary) || 0,
        fuel: parseFloat(formData.fuel) || 0,
        tolls: parseFloat(formData.tolls) || 0,
      };
      
      console.log('Отправляемые данные (исторические):', data);
      onSubmit(data);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {!isCurrentData && (
        <Input
          label="Период (дата и время)"
          name="period_month"
          type="datetime-local"
          value={formData.period_month}
          onChange={handleChange}
          required
        />
      )}
      
      <Input
        label="Имя водителя"
        name="driver_name"
        type="text"
        value={formData.driver_name}
        onChange={handleChange}
        placeholder="Введите имя водителя"
      />
      
      <Input
        label="Общая выручка"
        name="total_rev"
        type="number"
        step="0.01"
        value={formData.total_rev}
        onChange={handleChange}
        placeholder="0.00"
      />
      
      <Input
        label="Общий пробег (мили)"
        name="total_miles"
        type="number"
        value={formData.total_miles}
        onChange={handleChange}
        placeholder="0"
      />
      
      <Input
        label="Зарплата"
        name="salary"
        type="number"
        step="0.01"
        value={formData.salary}
        onChange={handleChange}
        placeholder="0.00"
      />
      
      <Input
        label="Топливо"
        name="fuel"
        type="number"
        step="0.01"
        value={formData.fuel}
        onChange={handleChange}
        placeholder="0.00"
      />
      
      <Input
        label="Платные дороги"
        name="tolls"
        type="number"
        step="0.01"
        value={formData.tolls}
        onChange={handleChange}
        placeholder="0.00"
      />
      
      <div className="flex justify-end space-x-3">
        {onCancel && (
          <Button
            type="button"
            variant="secondary"
            onClick={onCancel}
            disabled={loading}
          >
            Отмена
          </Button>
        )}
        <Button
          type="submit"
          variant="primary"
          loading={loading}
        >
          Сохранить
        </Button>
      </div>
    </form>
  );
};

export default VariableCostsForm;

