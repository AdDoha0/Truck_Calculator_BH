import React, { useState, useEffect } from 'react';
import Button from '../../../shared/ui/Button';
import Input from '../../../shared/ui/Input';
import type { FixedCostsCommon } from '../../../types';

interface CommonCostsFormProps {
  costs?: FixedCostsCommon;
  onSubmit: (data: Partial<FixedCostsCommon>) => void;
  onCancel?: () => void;
  loading?: boolean;
}

const CommonCostsForm: React.FC<CommonCostsFormProps> = ({
  costs,
  onSubmit,
  onCancel,
  loading = false,
}) => {
  const [formData, setFormData] = useState({
    ifta: '0',
    insurance: '0',
    eld: '0',
    tablet: '0',
    tolls: '0',
  });

  useEffect(() => {
    if (costs) {
      setFormData({
        ifta: costs.ifta.toString(),
        insurance: costs.insurance.toString(),
        eld: costs.eld.toString(),
        tablet: costs.tablet.toString(),
        tolls: costs.tolls.toString(),
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
    
    const data = {
      ifta: parseFloat(formData.ifta) || 0,
      insurance: parseFloat(formData.insurance) || 0,
      eld: parseFloat(formData.eld) || 0,
      tablet: parseFloat(formData.tablet) || 0,
      tolls: parseFloat(formData.tolls) || 0,
    };
    
    onSubmit(data);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="IFTA"
        name="ifta"
        type="number"
        step="0.01"
        value={formData.ifta}
        onChange={handleChange}
        placeholder="0.00"
      />
      
      <Input
        label="Страхование"
        name="insurance"
        type="number"
        step="0.01"
        value={formData.insurance}
        onChange={handleChange}
        placeholder="0.00"
      />
      
      <Input
        label="ELD"
        name="eld"
        type="number"
        step="0.01"
        value={formData.eld}
        onChange={handleChange}
        placeholder="0.00"
      />
      
      <Input
        label="Планшет"
        name="tablet"
        type="number"
        step="0.01"
        value={formData.tablet}
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

export default CommonCostsForm;

