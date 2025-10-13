import React, { useState } from 'react';
import Card from '../../../shared/ui/Card';
import Button from '../../../shared/ui/Button';
import Modal from '../../../shared/ui/Modal';
import CommonCostsForm from '../../../features/costs/components/CommonCostsForm';
import { useApi, useApiMutation } from '../../../shared/hooks/useApi';
import { costsApi } from '../../../features/costs/api/costsApi';
import type { FixedCostsCommon } from '../../../types';

const CommonCostsSection: React.FC = () => {
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const { data: commonCosts, loading, refetch } = useApi(costsApi.getCommonCosts);
  const updateMutation = useApiMutation(costsApi.updateCommonCosts);

  const handleSubmit = async (data: Partial<FixedCostsCommon>) => {
    try {
      await updateMutation.mutate(data);
      setIsEditModalOpen(false);
      refetch();
    } catch (error) {
      console.error('Ошибка при сохранении общих затрат:', error);
    }
  };

  return (
    <>
      <Card title="Общие фиксированные затраты">
        <div className="space-y-3">
          {loading ? (
            <p className="text-secondary-500">Загрузка...</p>
          ) : commonCosts ? (
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <span className="text-secondary-600">IFTA:</span>
                <span className="ml-2 font-medium">${commonCosts.ifta}</span>
              </div>
              <div>
                <span className="text-secondary-600">Страхование:</span>
                <span className="ml-2 font-medium">${commonCosts.insurance}</span>
              </div>
              <div>
                <span className="text-secondary-600">ELD:</span>
                <span className="ml-2 font-medium">${commonCosts.eld}</span>
              </div>
              <div>
                <span className="text-secondary-600">Планшет:</span>
                <span className="ml-2 font-medium">${commonCosts.tablet}</span>
              </div>
              <div>
                <span className="text-secondary-600">Платные дороги:</span>
                <span className="ml-2 font-medium">${commonCosts.tolls}</span>
              </div>
            </div>
          ) : (
            <p className="text-secondary-500">Нет данных</p>
          )}
          
          <div className="pt-2">
            <Button
              variant="secondary"
              size="sm"
              onClick={() => setIsEditModalOpen(true)}
            >
              Редактировать
            </Button>
          </div>
        </div>
      </Card>

      <Modal
        isOpen={isEditModalOpen}
        onClose={() => setIsEditModalOpen(false)}
        title="Редактировать общие затраты"
      >
        <CommonCostsForm
          costs={commonCosts}
          onSubmit={handleSubmit}
          onCancel={() => setIsEditModalOpen(false)}
          loading={updateMutation.loading}
        />
      </Modal>
    </>
  );
};

export default CommonCostsSection;

