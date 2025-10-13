import React, { useState, useEffect } from 'react';
import Button from '../../../shared/ui/Button';
import Input from '../../../shared/ui/Input';
import type { TruckVariableCosts, TruckVariableCostsCreate } from '../../../types';

interface VariableCostsFormProps {
  costs?: TruckVariableCosts;
  truckId: number;
  onSubmit: (data: TruckVariableCostsCreate) => void;
  onCancel?: () => void;
  loading?: boolean;
}

const VariableCostsForm: React.FC<VariableCostsFormProps> = ({
  costs,
  truckId,
  onSubmit,
  onCancel,
  loading = false,
}) => {
  const [formData, setFormData] = useState({
    period_month: new Date().toISOString().slice(0, 7),
    driver_name: '',
    total_rev: '0',
    total_miles: '0',
    salary: '0',
    fuel: '0',
    tolls: '0',
  });

  useEffect(() => {
    if (costs) {
      // Преобразуем YYYY-MM-DD в YYYY-MM для input type="month"
      const periodMonth = costs.period_month.length > 7 
        ? costs.period_month.slice(0, 7) 
        : costs.period_month;
        
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
  }, [costs]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Преобразуем YYYY-MM в YYYY-MM-DD для Django DateField
    const periodMonth = formData.period_month.length === 7 
      ? `${formData.period_month}-01` 
      : formData.period_month;
    
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
    
    console.log('Отправляемые данные:', data);
    onSubmit(data);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Период (месяц)"
        name="period_month"
        type="month"
        value={formData.period_month}
        onChange={handleChange}
        required
      />
      
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

