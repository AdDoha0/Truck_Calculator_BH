import * as React from 'react';

const Header: React.FC = () => {
  return (
    <header className="bg-white shadow-sm border-b border-secondary-200">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <h1 className="text-2xl font-bold text-secondary-900">
              Система учёта прибыльности траков
            </h1>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-secondary-500">
              Добро пожаловать, Администратор
            </span>
            <button className="text-sm text-secondary-500 hover:text-secondary-700">
              Выйти
            </button>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;

