import * as React from 'react';
import OverviewSection from './sections/OverviewSection';
import ProfitabilitySection from './sections/ProfitabilitySection';
import ChartsSection from './sections/ChartsSection';

const DashboardPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-secondary-900">Дашборд</h1>
        <p className="text-secondary-600 mt-1">
          Обзор прибыльности и ключевые показатели
        </p>
      </div>
      
      <OverviewSection />
      <ProfitabilitySection />
      <ChartsSection />
    </div>
  );
};

export default DashboardPage;

