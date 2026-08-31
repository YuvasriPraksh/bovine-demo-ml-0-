import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { DashboardView } from './views/DashboardView';
import { SurveillanceView } from './views/SurveillanceView';
import { PredictorView } from './views/PredictorView';
import { ModelPerformanceView } from './views/ModelPerformanceView';
import { AlertsView } from './views/AlertsView';
import { AnimalDetailView } from './views/AnimalDetailView';
import { LoginView } from './views/LoginView';
import { RegisterCowModal } from './components/RegisterCowModal';
import { fetchDashboardSummary } from './services/api';

export function App() {
  const [user, setUser] = useState({
    username: 'admin',
    name: 'Dr. Ramesh Sharma',
    role: 'Chief Herd Veterinarian',
    farm: 'Amul Dairy Research Station',
  });

  const [activeTab, setActiveTab] = useState('dashboard');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedAnimalId, setSelectedAnimalId] = useState(null);
  const [showRegisterModal, setShowRegisterModal] = useState(false);

  const [dashboardData, setDashboardData] = useState(null);
  const [loadingDashboard, setLoadingDashboard] = useState(true);

  const loadDashboard = async () => {
    setLoadingDashboard(true);
    try {
      const data = await fetchDashboardSummary();
      setDashboardData(data);
    } catch (err) {
      console.error('Error fetching dashboard summary:', err);
    } finally {
      setLoadingDashboard(false);
    }
  };

  useEffect(() => {
    if (user) {
      loadDashboard();
    }
  }, [user]);

  if (!user) {
    return <LoginView onLoginSuccess={(loggedInUser) => setUser(loggedInUser)} />;
  }

  return (
    <div className="flex min-h-screen bg-slate-50 font-sans antialiased text-slate-900">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        user={user}
        onLogout={() => setUser(null)}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Header Navigation */}
        <Header
          activeTab={activeTab}
          searchTerm={searchTerm}
          setSearchTerm={setSearchTerm}
          onSelectAnimal={(id) => setSelectedAnimalId(id)}
          user={user}
          onLogout={() => setUser(null)}
          onOpenRegisterModal={() => setShowRegisterModal(true)}
        />

        {/* View Body */}
        <main className="p-6 flex-1">
          {activeTab === 'dashboard' && (
            <DashboardView
              data={dashboardData}
              onSelectAnimal={(id) => setSelectedAnimalId(id)}
              onNavigate={(tab) => setActiveTab(tab)}
              onOpenRegisterModal={() => setShowRegisterModal(true)}
            />
          )}

          {activeTab === 'surveillance' && (
            <SurveillanceView
              onSelectAnimal={(id) => setSelectedAnimalId(id)}
              onOpenRegisterModal={() => setShowRegisterModal(true)}
            />
          )}

          {activeTab === 'predictor' && <PredictorView />}

          {activeTab === 'alerts' && (
            <AlertsView onSelectAnimal={(id) => setSelectedAnimalId(id)} />
          )}

          {activeTab === 'performance' && <ModelPerformanceView />}
        </main>
      </div>

      {/* Animal Inspection Detail Modal */}
      {selectedAnimalId && (
        <AnimalDetailView
          animalId={selectedAnimalId}
          onClose={() => setSelectedAnimalId(null)}
        />
      )}

      {/* Register New Cow Modal */}
      {showRegisterModal && (
        <RegisterCowModal
          onClose={() => setShowRegisterModal(false)}
          onSuccess={() => {
            loadDashboard();
          }}
        />
      )}
    </div>
  );
}

export default App;
