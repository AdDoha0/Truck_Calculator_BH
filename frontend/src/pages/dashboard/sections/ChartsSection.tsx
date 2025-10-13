import * as React from 'react';
import Card from '../../../shared/ui/Card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';

// Временные данные для демонстрации
const profitData = [
  { month: 'Янв', profit: 45000, revenue: 200000 },
  { month: 'Фев', profit: 52000, revenue: 220000 },
  { month: 'Мар', profit: 48000, revenue: 210000 },
  { month: 'Апр', profit: 61000, revenue: 250000 },
  { month: 'Май', profit: 55000, revenue: 230000 },
  { month: 'Июн', profit: 67000, revenue: 260000 },
];

const truckData = [
  { name: 'TR-001', profit: 50000, margin: 20.4 },
  { name: 'TR-002', profit: 80000, margin: 25.0 },
  { name: 'TR-003', profit: 20000, margin: 11.1 },
  { name: 'TR-004', profit: 65000, margin: 22.5 },
];

const ChartsSection: React.FC = () => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <Card title="Тренд прибыли по месяцам">
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={profitData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip 
                formatter={(value, name) => [
                  `₽${Number(value).toLocaleString()}`,
                  name === 'profit' ? 'Прибыль' : 'Выручка'
                ]}
              />
              <Line 
                type="monotone" 
                dataKey="profit" 
                stroke="#3b82f6" 
                strokeWidth={2}
                name="profit"
              />
              <Line 
                type="monotone" 
                dataKey="revenue" 
                stroke="#10b981" 
                strokeWidth={2}
                name="revenue"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </Card>

      <Card title="Прибыль по тракам">
        <div className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={truckData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip 
                formatter={(value) => [`₽${Number(value).toLocaleString()}`, 'Прибыль']}
              />
              <Bar dataKey="profit" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </Card>
    </div>
  );
};

export default ChartsSection;

