import * as React from 'react';
import Header from './Header';
import Sidebar from './Sidebar';

interface MainLayoutProps {
  children: React.ReactNode;
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const [isSidebarOpen, setIsSidebarOpen] = React.useState(true);

  const handleToggleSidebar = () => setIsSidebarOpen((prev) => !prev);

  return (
    <div className="min-h-screen bg-secondary-50">
      <Header onToggleSidebar={handleToggleSidebar} isSidebarOpen={isSidebarOpen} />
      <div className="flex">
        <Sidebar collapsed={!isSidebarOpen} />
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>
    </div>
  );
};

export default MainLayout;

