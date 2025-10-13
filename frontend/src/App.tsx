import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './shared/layouts/MainLayout';
import DashboardPage from './pages/dashboard/DashboardPage';
import TrucksPage from './pages/trucks/TrucksPage';
import CostsPage from './pages/costs/CostsPage';
import SnapshotsPage from './pages/snapshots/SnapshotsPage';
import ReportsPage from './pages/reports/ReportsPage';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/trucks" element={<TrucksPage />} />
          <Route path="/costs" element={<CostsPage />} />
          <Route path="/snapshots" element={<SnapshotsPage />} />
          <Route path="/reports" element={<ReportsPage />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;