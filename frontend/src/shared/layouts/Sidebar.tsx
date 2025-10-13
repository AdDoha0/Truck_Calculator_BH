import * as React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar: React.FC = () => {
  const navigation = [
    { name: 'Дашборд', href: '/dashboard', icon: '📊' },
    { name: 'Траки', href: '/trucks', icon: '🚛' },
    { name: 'Стоимости', href: '/costs', icon: '💰' },
    { name: 'Снимки', href: '/snapshots', icon: '📸' },
    { name: 'Отчёты', href: '/reports', icon: '📈' },
  ];

  return (
    <nav className="w-64 bg-white shadow-sm border-r border-secondary-200 min-h-screen">
      <div className="p-4">
        <ul className="space-y-2">
          {navigation.map((item) => (
            <li key={item.name}>
              <NavLink
                to={item.href}
                className={({ isActive }) =>
                  `flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200 ${
                    isActive
                      ? 'bg-primary-100 text-primary-700 border-r-2 border-primary-600'
                      : 'text-secondary-600 hover:bg-secondary-100 hover:text-secondary-900'
                  }`
                }
              >
                <span className="mr-3 text-lg">{item.icon}</span>
                {item.name}
              </NavLink>
            </li>
          ))}
        </ul>
      </div>
    </nav>
  );
};

export default Sidebar;

