import React from 'react';
import {
  LayoutDashboard,
  Activity,
  Cpu,
  BarChart3,
  AlertTriangle,
  ShieldCheck,
  ChevronRight,
} from 'lucide-react';

export const Sidebar = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'dashboard', label: 'Herd Overview', icon: LayoutDashboard },
    { id: 'surveillance', label: 'Herd Surveillance', icon: Activity },
    { id: 'predictor', label: 'AI Prediction Console', icon: Cpu, highlight: true },
    { id: 'alerts', label: 'High-Risk Alerts', icon: AlertTriangle },
    { id: 'performance', label: 'Model Evaluation', icon: BarChart3 },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-white min-h-screen flex flex-col justify-between shrink-0 border-r border-slate-800">
      <div>
        {/* Brand Header */}
        <div className="p-5 border-b border-slate-800 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center text-white shadow-lg shadow-emerald-500/20">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-extrabold text-base tracking-tight text-white flex items-center gap-1">
              BovineGuard <span className="text-emerald-400 text-xs font-mono font-bold px-1.5 py-0.5 rounded bg-emerald-500/10 border border-emerald-500/20">AI</span>
            </h1>
            <p className="text-[11px] text-slate-400 font-medium">
              Govt. of India Early Warning
            </p>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="p-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl font-semibold text-xs transition-all ${
                  isActive
                    ? 'bg-emerald-500 text-white shadow-md shadow-emerald-500/20'
                    : item.highlight
                    ? 'bg-slate-800/80 text-emerald-400 hover:bg-slate-800 border border-emerald-500/30'
                    : 'text-slate-400 hover:bg-slate-800/60 hover:text-white'
                }`}
              >
                <div className="flex items-center gap-2.5">
                  <Icon className="w-4 h-4" />
                  <span>{item.label}</span>
                </div>
                {isActive && <ChevronRight className="w-3.5 h-3.5 opacity-80" />}
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer Info */}
      <div className="p-4 border-t border-slate-800 text-[11px] text-slate-500 space-y-1">
        <div className="flex items-center justify-between">
          <span>Engine Status</span>
          <span className="flex items-center gap-1 text-emerald-400 font-medium">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping" />
            Active
          </span>
        </div>
        <p className="text-[10px] text-slate-600">
          XGBoost ML Pipeline v1.0.0
        </p>
      </div>
    </aside>
  );
};
