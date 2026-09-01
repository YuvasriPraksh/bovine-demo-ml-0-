import React from 'react';
import { Search, PlusCircle, LogOut, UserCheck, Volume2, Globe } from 'lucide-react';
import { t, setLanguage, getLanguage } from '../utils/i18n';
import { speakText } from '../utils/tts';

export const Header = ({
  activeTab,
  searchTerm,
  setSearchTerm,
  onSelectAnimal,
  user,
  onLogout,
  onOpenRegisterModal,
  appMode,
  setAppMode
}) => {
  const currentLang = getLanguage();

  const handleLanguageChange = (e) => {
    setLanguage(e.target.value);
    window.location.reload(); // Simple way to re-render whole app with new language for now
  };

  const handleVoice = () => {
    // A simple generic voice action for the header if needed, 
    // or it just acts as a global voice toggle.
    speakText(t('greeting_desc'));
  };

  return (
    <header className="bg-white border-b border-slate-200/80 px-4 md:px-6 py-3 flex items-center justify-between sticky top-0 z-30 shadow-sm">
      <div className="flex items-center gap-2">
        <h2 className="text-xl md:text-2xl font-extrabold text-emerald-800 tracking-tight flex items-center gap-2">
          🐄 <span>{t('app_title')}</span>
        </h2>
      </div>

      <div className="flex items-center gap-3 md:gap-4">
        {/* Language Selector */}
        <div className="flex items-center bg-slate-100 rounded-lg px-2 py-1">
          <Globe className="w-4 h-4 text-slate-500 mr-1" />
          <select 
            value={currentLang}
            onChange={handleLanguageChange}
            className="bg-transparent text-sm font-bold text-slate-700 outline-none cursor-pointer"
          >
            <option value="en">English</option>
            <option value="ta">தமிழ்</option>
            <option value="hi">हिन्दी</option>
            <option value="te">తెలుగు</option>
            <option value="kn">ಕನ್ನಡ</option>
          </select>
        </div>

        {/* Global Voice Button */}
        <button 
          onClick={handleVoice}
          className="p-2 bg-emerald-100 text-emerald-700 rounded-full hover:bg-emerald-200 transition shadow-sm"
          title="Listen"
        >
          <Volume2 className="w-5 h-5" />
        </button>

        {/* Desktop Only Actions */}
        <div className="hidden md:flex items-center gap-3">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder={t('search_placeholder')}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && searchTerm.trim()) {
                  const id = parseInt(searchTerm.replace(/\D/g, ''), 10);
                  if (id) onSelectAnimal(id);
                }
              }}
              className="pl-9 pr-4 py-1.5 w-48 text-sm font-medium bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 transition-all"
            />
          </div>

          <button
            onClick={onOpenRegisterModal}
            className="px-3 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-sm flex items-center gap-1.5 shadow-sm transition"
          >
            <PlusCircle className="w-4 h-4" />
            <span>{t('register_cow')}</span>
          </button>
        </div>

        {/* User / Mode Toggle */}
        {user && (
          <div className="flex items-center gap-2 pl-2 border-l border-slate-200">
             <select 
                value={appMode}
                onChange={(e) => setAppMode(e.target.value)}
                className="hidden md:block bg-slate-50 border border-slate-200 text-xs font-bold text-slate-700 rounded-lg px-2 py-1 outline-none cursor-pointer"
              >
                <option value="farmer">{t('farmer_mode_toggle')}</option>
                <option value="expert">{t('expert_mode_toggle')}</option>
              </select>
            <button
              onClick={onLogout}
              title="Sign Out"
              className="p-2 rounded-xl text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition"
            >
              <LogOut className="w-5 h-5" />
            </button>
          </div>
        )}
      </div>
    </header>
  );
};
