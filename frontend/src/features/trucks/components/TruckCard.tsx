import React from 'react';
import Button from '../../../shared/ui/Button';
import type { Truck, TruckVariableCosts, FixedCostsTruck } from '../../../types';

interface TruckCardProps {
  truck: Truck;
  variableCosts?: TruckVariableCosts;
  fixedCosts?: FixedCostsTruck;
  onEdit: (truck: Truck) => void;
  onDelete: (truck: Truck) => void;
  onViewDetails: (truck: Truck) => void;
}

const TruckCard: React.FC<TruckCardProps> = ({
  truck,
  variableCosts,
  fixedCosts,
  onEdit,
  onDelete,
  onViewDetails,
}) => {
  // Определяем тип прицепа из фиксированных затрат (если есть)
  const trailerType = fixedCosts?.trailer_payment ? 'Reefer' : 'Dry Van';
  
  return (
    <div className="bg-white border border-secondary-200 rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-xl font-bold text-secondary-900">{truck.tractor_no}</h3>
        <div className="flex space-x-1">
          <button
            onClick={() => onViewDetails(truck)}
            className="p-1 text-primary-600 hover:bg-primary-50 rounded"
            title="Открыть детали"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
          </button>
          <button
            onClick={() => onEdit(truck)}
            className="p-1 text-secondary-600 hover:bg-secondary-50 rounded"
            title="Редактировать"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
          </button>
          <button
            onClick={() => onDelete(truck)}
            className="p-1 text-red-600 hover:bg-red-50 rounded"
            title="Удалить"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>

      <div className="space-y-2">
        <div className="grid grid-cols-2 gap-2">
          <div>
            <p className="text-xs text-secondary-500">Период расчета</p>
            <p className="text-sm font-medium">
              {variableCosts?.period_month ? new Date(variableCosts.period_month).toLocaleDateString('ru-RU', { year: 'numeric', month: 'long' }) : 'Месячный'}
            </p>
          </div>
          <div>
            <p className="text-xs text-secondary-500">Тип прицепа</p>
            <p className="text-sm font-medium">{trailerType}</p>
          </div>
        </div>

        {variableCosts && (
          <div className="pt-2 border-t border-secondary-100">
            <p className="text-xs text-secondary-500">Предыдущий период</p>
            <p className="text-sm font-medium">
              {new Date(new Date(variableCosts.period_month).setMonth(new Date(variableCosts.period_month).getMonth() - 1)).toLocaleDateString('ru-RU', { year: 'numeric', month: 'long' })}
            </p>
            {variableCosts.driver_name && (
              <p className="text-xs text-secondary-600 mt-1">Водитель: {variableCosts.driver_name}</p>
            )}
          </div>
        )}

        {!variableCosts && (
          <div className="pt-2 border-t border-secondary-100">
            <p className="text-xs text-secondary-500 italic">Нет данных о затратах</p>
          </div>
        )}
      </div>

      <div className="mt-3 pt-3 border-t border-secondary-100">
        <Button
          variant="primary"
          size="sm"
          onClick={() => onViewDetails(truck)}
          className="w-full"
        >
          Открыть детали
        </Button>
      </div>
    </div>
  );
};

export default TruckCard;

