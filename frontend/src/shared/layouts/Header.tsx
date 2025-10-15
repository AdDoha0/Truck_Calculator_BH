import * as React from 'react';

interface HeaderProps {
  onToggleSidebar?: () => void;
  isSidebarOpen?: boolean;
}

const Header: React.FC<HeaderProps> = ({ onToggleSidebar, isSidebarOpen }) => {
  return (
    <header className="bg-white shadow-sm border-b border-secondary-200">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <button
              type="button"
              onClick={onToggleSidebar}
              aria-label="Переключить сайдбар"
              className="mr-4 inline-flex h-9 w-9 items-center justify-center rounded-md border border-secondary-300 text-secondary-700 hover:bg-secondary-100 focus:outline-none"
            >
              <span className="text-lg" role="img" aria-hidden>
                {isSidebarOpen ? '⟨' : '☰'}
              </span>
            </button>
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

