import React, { useState, useEffect } from 'react';
import Button from '../../../shared/ui/Button';
import Input from '../../../shared/ui/Input';
import type { Truck, TruckCreate } from '../types';

interface TruckFormProps {
  truck?: Truck;
  onSubmit: (data: TruckCreate) => void;
  onCancel: () => void;
  loading?: boolean;
}

const TruckForm: React.FC<TruckFormProps> = ({
  truck,
  onSubmit,
  onCancel,
  loading = false,
}) => {
  const [formData, setFormData] = useState<TruckCreate>({
    tractor_no: '',
  });
  const [errors, setErrors] = useState<Partial<TruckCreate>>({});

  useEffect(() => {
    if (truck) {
      setFormData({
        tractor_no: truck.tractor_no,
      });
    }
  }, [truck]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
    
    // Clear error when user starts typing
    if (errors[name as keyof TruckCreate]) {
      setErrors(prev => ({
        ...prev,
        [name]: undefined,
      }));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    const newErrors: Partial<TruckCreate> = {};
    if (!formData.tractor_no.trim()) {
      newErrors.tractor_no = 'Номер трактора обязателен';
    }
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }
    
    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Номер трактора"
        name="tractor_no"
        value={formData.tractor_no}
        onChange={handleChange}
        error={errors.tractor_no}
        placeholder="Введите номер трактора"
        required
      />
      
      <div className="flex justify-end space-x-3">
        <Button
          type="button"
          variant="secondary"
          onClick={onCancel}
          disabled={loading}
        >
          Отмена
        </Button>
        <Button
          type="submit"
          variant="primary"
          loading={loading}
        >
          {truck ? 'Обновить' : 'Создать'}
        </Button>
      </div>
    </form>
  );
};

export default TruckForm;
