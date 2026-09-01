import React from 'react';
import { Home, List, Bell, Info } from 'lucide-react';
import { t } from '../utils/i18n';

export function BottomNav({ activeTab, setActiveTab }) {
  const navItems = [
    { id: 'dashboard', label: t('nav_home'), Icon: Home },
    { id: 'surveillance', label: t('nav_my_cows'), Icon: List },
    { id: 'alerts', label: t('nav_alerts'), Icon: Bell },
    { id: 'help', label: t('nav_help'), Icon: Info }
  ];

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-slate-200 z-50 px-2 pb-safe shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)] md:hidden">
      <div className="flex justify-around items-center h-16">
        {navItems.map(({ id, label, Icon }) => {
          const isActive = activeTab === id;
          return (
            <button
              key={id}
              onClick={() => setActiveTab(id)}
              className={`flex flex-col items-center justify-center w-full h-full space-y-1 ${
                isActive ? 'text-emerald-600' : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              <Icon className={`w-6 h-6 ${isActive ? 'stroke-2' : 'stroke-[1.5]'}`} />
              <span className="text-[10px] font-bold tracking-wide">{label}</span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
