import React, { useState, useEffect } from 'react';
import Button from '../../../shared/ui/Button';
import Input from '../../../shared/ui/Input';
import type { FixedCostsTruck, FixedCostsTruckCreate } from '../../../types';

interface FixedCostsFormProps {
  costs?: FixedCostsTruck;
  truckId: number;
  onSubmit: (data: FixedCostsTruckCreate) => void;
  onCancel?: () => void;
  loading?: boolean;
}

const FixedCostsForm: React.FC<FixedCostsFormProps> = ({
  costs,
  truckId,
  onSubmit,
  onCancel,
  loading = false,
}) => {
  const [formData, setFormData] = useState({
    truck_payment: '0',
    trailer_payment: '0',
    physical_damage_insurance_truck: '0',
    physical_damage_insurance_trailer: '0',
  });

  useEffect(() => {
    if (costs) {
      setFormData({
        truck_payment: (costs.truck_payment || 0).toString(),
        trailer_payment: (costs.trailer_payment || 0).toString(),
        physical_damage_insurance_truck: (costs.physical_damage_insurance_truck || 0).toString(),
        physical_damage_insurance_trailer: (costs.physical_damage_insurance_trailer || 0).toString(),
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
    
    const data: FixedCostsTruckCreate = {
      truck: truckId,
      truck_payment: parseFloat(formData.truck_payment) || 0,
      trailer_payment: parseFloat(formData.trailer_payment) || 0,
      physical_damage_insurance_truck: parseFloat(formData.physical_damage_insurance_truck) || 0,
      physical_damage_insurance_trailer: parseFloat(formData.physical_damage_insurance_trailer) || 0,
    };
    
    onSubmit(data);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Платеж за трак"
        name="truck_payment"
        type="number"
        step="0.01"
        value={formData.truck_payment}
        onChange={handleChange}
        placeholder="0.00"
      />
      
      <Input
        label="Платеж за прицеп"
        name="trailer_payment"
        type="number"
        step="0.01"
        value={formData.trailer_payment}
        onChange={handleChange}
        placeholder="0.00"
      />
      
      <Input
        label="Страхование физического ущерба трака"
        name="physical_damage_insurance_truck"
        type="number"
        step="0.01"
        value={formData.physical_damage_insurance_truck}
        onChange={handleChange}
        placeholder="0.00"
      />
      
      <Input
        label="Страхование физического ущерба прицепа"
        name="physical_damage_insurance_trailer"
        type="number"
        step="0.01"
        value={formData.physical_damage_insurance_trailer}
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

export default FixedCostsForm;

