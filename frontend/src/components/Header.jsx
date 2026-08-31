import React from 'react';
import { Search, PlusCircle, LogOut, UserCheck } from 'lucide-react';

export const Header = ({
  activeTab,
  searchTerm,
  setSearchTerm,
  onSelectAnimal,
  user,
  onLogout,
  onOpenRegisterModal,
}) => {
  const titles = {
    dashboard: 'National Dairy Herd Risk Dashboard',
    surveillance: 'Herd Surveillance & Livestock Telemetry',
    predictor: 'AI Mastitis Prediction & Live IoT Console',
    alerts: 'Critical Decision-Support Alerts',
    performance: 'Model Performance & Benchmark Console',
  };

  return (
    <header className="bg-white border-b border-slate-200/80 px-6 py-4 flex items-center justify-between sticky top-0 z-30 shadow-2xs">
      <div>
        <h2 className="text-lg font-extrabold text-slate-900 tracking-tight flex items-center gap-2">
          <span>{titles[activeTab] || 'BovineGuard AI Portal'}</span>
          <span className="px-2 py-0.5 text-[10px] font-bold uppercase rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200">
            Live Stream
          </span>
        </h2>
        <p className="text-xs text-slate-500 font-medium mt-0.5">
          Real-Time Subclinical Risk Forecasting · Department of Animal Husbandry & Dairying
        </p>
      </div>

      <div className="flex items-center gap-3">
        {/* Quick Search */}
        <div className="relative hidden md:block">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search Cow ID (e.g. 12001)..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && searchTerm.trim()) {
                const id = parseInt(searchTerm.replace(/\D/g, ''), 10);
                if (id) onSelectAnimal(id);
              }
            }}
            className="pl-9 pr-4 py-1.5 w-56 text-xs font-medium bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all"
          />
        </div>

        {/* Register New Cow Button */}
        <button
          onClick={onOpenRegisterModal}
          className="px-3 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs flex items-center gap-1.5 shadow-xs transition"
        >
          <PlusCircle className="w-4 h-4" />
          <span>Register New Cow</span>
        </button>

        {/* User Profile & Logout */}
        {user && (
          <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
            <div className="text-right hidden xl:block">
              <span className="text-xs font-extrabold text-slate-900 block leading-tight">
                {user.name}
              </span>
              <span className="text-[10px] text-slate-500 block leading-tight font-medium">
                {user.role}
              </span>
            </div>
            <button
              onClick={onLogout}
              title="Sign Out"
              className="p-2 rounded-xl text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        )}
      </div>
    </header>
  );
};
