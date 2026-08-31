import React from 'react';

export const RiskBadge = ({ category, score = null, size = 'md' }) => {
  const normCat = (category || 'No_Risk').toString().replace(/\s+/g, '_');

  const config = {
    No_Risk: {
      label: 'No Risk',
      bg: 'bg-emerald-50 border-emerald-200 text-emerald-700',
      dot: 'bg-emerald-500',
    },
    Low: {
      label: 'Low Risk',
      bg: 'bg-sky-50 border-sky-200 text-sky-700',
      dot: 'bg-sky-500',
    },
    Moderate: {
      label: 'Moderate Risk',
      bg: 'bg-amber-50 border-amber-200 text-amber-700',
      dot: 'bg-amber-500',
    },
    High: {
      label: 'High Risk Alert',
      bg: 'bg-rose-50 border-rose-200 text-rose-700 font-bold animate-pulse',
      dot: 'bg-rose-500',
    },
  };

  const current = config[normCat] || config.No_Risk;
  const sizeClasses = size === 'sm' ? 'px-2 py-0.5 text-[11px]' : 'px-3 py-1 text-xs';

  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full border font-semibold ${current.bg} ${sizeClasses}`}
    >
      <span className={`w-2 h-2 rounded-full shrink-0 ${current.dot}`} />
      <span>{current.label}</span>
      {score !== null && (
        <span className="font-mono opacity-85 ml-0.5">({score}%)</span>
      )}
    </span>
  );
};
