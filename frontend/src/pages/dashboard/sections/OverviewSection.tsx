import * as React from 'react';
import Card from '../../../shared/ui/Card';

const OverviewSection: React.FC = () => {
  // Временные данные для демонстрации
  const stats = [
    {
      title: 'Всего траков',
      value: '12',
      change: '+2',
      changeType: 'positive' as const,
      icon: '🚛',
    },
    {
      title: 'Общая выручка',
      value: '₽2,450,000',
      change: '+12%',
      changeType: 'positive' as const,
      icon: '💰',
    },
    {
      title: 'Общая прибыль',
      value: '₽580,000',
      change: '+8%',
      changeType: 'positive' as const,
      icon: '📈',
    },
    {
      title: 'Средняя маржа',
      value: '23.7%',
      change: '-1.2%',
      changeType: 'negative' as const,
      icon: '📊',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat, index) => (
        <Card key={index} className="p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <span className="text-3xl">{stat.icon}</span>
            </div>
            <div className="ml-4 flex-1">
              <p className="text-sm font-medium text-secondary-600">
                {stat.title}
              </p>
              <div className="flex items-baseline">
                <p className="text-2xl font-semibold text-secondary-900">
                  {stat.value}
                </p>
                <p
                  className={`ml-2 text-sm font-medium ${
                    stat.changeType === 'positive'
                      ? 'text-green-600'
                      : 'text-red-600'
                  }`}
                >
                  {stat.change}
                </p>
              </div>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
};

export default OverviewSection;

