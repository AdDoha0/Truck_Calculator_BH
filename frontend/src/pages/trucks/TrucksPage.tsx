import React, { useState } from 'react';
import TruckListSection from './sections/TruckListSection';
import TruckFormSection from './sections/TruckFormSection';

const TrucksPage: React.FC = () => {
  const [showForm, setShowForm] = useState(false);
  const [editingTruck, setEditingTruck] = useState<any>(null);

  const handleEdit = (truck: any) => {
    setEditingTruck(truck);
    setShowForm(true);
  };

  const handleDelete = (truck: any) => {
    if (window.confirm(`Вы уверены, что хотите удалить трак ${truck.tractor_no}?`)) {
      // TODO: Implement delete logic
      console.log('Delete truck:', truck);
    }
  };

  const handleFormSubmit = (data: any) => {
    console.log('Form submitted:', data);
    setShowForm(false);
    setEditingTruck(null);
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingTruck(null);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-secondary-900">Траки</h1>
          <p className="text-secondary-600 mt-1">
            Управление траками и их данными
          </p>
        </div>
        <button
          onClick={() => setShowForm(true)}
          className="btn btn-primary"
        >
          Добавить трак
        </button>
      </div>

      {showForm && (
        <TruckFormSection
          truck={editingTruck}
          onSubmit={handleFormSubmit}
          onCancel={handleFormCancel}
        />
      )}

      <TruckListSection
        onEdit={handleEdit}
        onDelete={handleDelete}
      />
    </div>
  );
};

export default TrucksPage;

