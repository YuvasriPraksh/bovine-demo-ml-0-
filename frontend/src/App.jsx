import React, { useState, useEffect } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { BottomNav } from './components/BottomNav';
import { DashboardView } from './views/DashboardView';
import { SurveillanceView } from './views/SurveillanceView';
import { PredictorView } from './views/PredictorView';
import { ModelPerformanceView } from './views/ModelPerformanceView';
import { AlertsView } from './views/AlertsView';
import { AnimalDetailView } from './views/AnimalDetailView';
import { LoginView } from './views/LoginView';
import { RegisterCowModal } from './components/RegisterCowModal';
import { fetchDashboardSummary } from './services/api';

// New Farmer-first Views
import { FarmerDashboardView } from './views/FarmerDashboardView';
import { MyCowsView } from './views/MyCowsView';
import { CowDetailMobileView } from './views/CowDetailMobileView';
import { t } from './utils/i18n';

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
  
  // App Mode State: 'farmer' (default simple view) or 'expert' (analytical view)
  const [appMode, setAppMode] = useState('farmer');

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

  // Determine if we should show the offline banner (stub for now)
  const isOffline = !navigator.onLine;

  return (
    <div className="flex min-h-screen bg-slate-50 font-sans antialiased text-slate-900">
      
      {/* Sidebar Navigation - Hidden on Mobile, only visible on Desktop Expert Mode */}
      {appMode === 'expert' && (
        <div className="hidden md:block">
          <Sidebar
            activeTab={activeTab}
            setActiveTab={setActiveTab}
            user={user}
            onLogout={() => setUser(null)}
          />
        </div>
      )}

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 pb-16 md:pb-0">
        
        {/* Offline Banner */}
        {isOffline && (
          <div className="bg-amber-100 text-amber-800 text-xs font-bold text-center py-1 border-b border-amber-200 sticky top-0 z-40">
            ⚠️ {t('offline_message')}
          </div>
        )}

        {/* Header Navigation */}
        <Header
          activeTab={activeTab}
          searchTerm={searchTerm}
          setSearchTerm={setSearchTerm}
          onSelectAnimal={(id) => setSelectedAnimalId(id)}
          user={user}
          onLogout={() => setUser(null)}
          onOpenRegisterModal={() => setShowRegisterModal(true)}
          appMode={appMode}
          setAppMode={setAppMode}
        />

        {/* View Body */}
        <main className="p-4 md:p-6 flex-1 overflow-x-hidden">
          
          {/* Dashboard Tab */}
          {activeTab === 'dashboard' && (
            appMode === 'expert' ? (
              <DashboardView
                data={dashboardData}
                onSelectAnimal={(id) => setSelectedAnimalId(id)}
                onNavigate={(tab) => setActiveTab(tab)}
                onOpenRegisterModal={() => setShowRegisterModal(true)}
              />
            ) : (
              <FarmerDashboardView 
                data={dashboardData}
                onSelectAnimal={(id) => setSelectedAnimalId(id)}
              />
            )
          )}

          {/* Surveillance / My Cows Tab */}
          {activeTab === 'surveillance' && (
            appMode === 'expert' ? (
              <SurveillanceView
                onSelectAnimal={(id) => setSelectedAnimalId(id)}
                onOpenRegisterModal={() => setShowRegisterModal(true)}
              />
            ) : (
              <MyCowsView onSelectAnimal={(id) => setSelectedAnimalId(id)} />
            )
          )}

          {/* Predictor Tab - Expert Only */}
          {activeTab === 'predictor' && (
            appMode === 'expert' ? <PredictorView /> : <div className="text-center py-10 text-slate-500">Switch to Expert Mode to view Live Predictor.</div>
          )}

          {/* Alerts Tab */}
          {activeTab === 'alerts' && (
            <AlertsView onSelectAnimal={(id) => setSelectedAnimalId(id)} />
          )}

          {/* Performance Tab - Expert Only */}
          {activeTab === 'performance' && (
             appMode === 'expert' ? <ModelPerformanceView /> : <div className="text-center py-10 text-slate-500">Switch to Expert Mode to view Model Performance.</div>
          )}
          
          {/* Help Tab Placeholder for Farmer Mode */}
          {activeTab === 'help' && (
             <div className="max-w-md mx-auto text-center py-12">
               <div className="text-6xl mb-4">👨‍⚕️</div>
               <h2 className="text-xl font-bold text-slate-800 mb-2">Veterinary Support</h2>
               <p className="text-slate-600 mb-6">Need help with a sick cow? Contact your local dairy department veterinarian.</p>
               <button className="bg-emerald-600 text-white font-bold py-3 px-6 rounded-xl w-full">Call Support</button>
             </div>
          )}
        </main>
      </div>
      
      {/* Mobile Bottom Navigation - Only visible on Mobile */}
      <BottomNav activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Animal Inspection Detail Modal */}
      {selectedAnimalId && (
        appMode === 'expert' ? (
          <AnimalDetailView
            animalId={selectedAnimalId}
            onClose={() => setSelectedAnimalId(null)}
          />
        ) : (
          <CowDetailMobileView 
            animalId={selectedAnimalId}
            onClose={() => setSelectedAnimalId(null)}
          />
        )
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
