import React from 'react';

export const StatCard = ({ title, value, subtext, icon: Icon, color = 'emerald' }) => {
  const themes = {
    emerald: 'bg-emerald-50/50 border-emerald-100 text-emerald-700 icon-bg-emerald-100',
    sky: 'bg-sky-50/50 border-sky-100 text-sky-700 icon-bg-sky-100',
    amber: 'bg-amber-50/50 border-amber-100 text-amber-700 icon-bg-amber-100',
    rose: 'bg-rose-50/50 border-rose-100 text-rose-700 icon-bg-rose-100',
    slate: 'bg-slate-50/50 border-slate-200 text-slate-700 icon-bg-slate-200',
  };

  const currentTheme = themes[color] || themes.emerald;

  return (
    <div className="bg-white border border-slate-200/90 rounded-2xl p-4 shadow-xs hover:shadow-md transition-all duration-200">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
            {title}
          </p>
          <h3 className="text-2xl font-extrabold font-mono text-slate-900 mt-1">
            {value}
          </h3>
          {subtext && (
            <p className="text-[11px] font-medium text-slate-500 mt-1">
              {subtext}
            </p>
          )}
        </div>
        {Icon && (
          <div className={`p-3 rounded-xl border ${currentTheme}`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>
    </div>
  );
};
