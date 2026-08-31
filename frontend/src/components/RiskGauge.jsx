import React from 'react';

export const RiskGauge = ({ score = 0, riskCategory = 'No_Risk' }) => {
  const clampedScore = Math.max(0, Math.min(100, Number(score) || 0));
  
  // Calculate SVG arc rotation angle (-90deg to +90deg)
  const angle = (clampedScore / 100) * 180 - 90;

  const getColor = (cat) => {
    switch (cat) {
      case 'High': return '#f43f5e';
      case 'Moderate': return '#f59e0b';
      case 'Low': return '#0ea5e9';
      default: return '#10b981';
    }
  };

  const strokeColor = getColor(riskCategory);

  return (
    <div className="relative flex flex-col items-center justify-center p-4">
      <svg className="w-48 h-28 overflow-visible" viewBox="0 0 200 110">
        {/* Background Track Arc */}
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="#e2e8f0"
          strokeWidth="16"
          strokeLinecap="round"
        />
        
        {/* Active Filled Arc */}
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke={strokeColor}
          strokeWidth="16"
          strokeLinecap="round"
          strokeDasharray="251.2"
          strokeDashoffset={251.2 - (clampedScore / 100) * 251.2}
          className="transition-all duration-1000 ease-out"
        />

        {/* Pointer Needle */}
        <g transform={`translate(100, 100) rotate(${angle})`}>
          <line
            x1="0"
            y1="0"
            x2="0"
            y2="-68"
            stroke="#0f172a"
            strokeWidth="3.5"
            strokeLinecap="round"
          />
          <circle cx="0" cy="0" r="7" fill="#0f172a" />
          <circle cx="0" cy="0" r="3" fill="#ffffff" />
        </g>
      </svg>

      {/* Score Text Overlay */}
      <div className="text-center -mt-6">
        <span className="text-3xl font-extrabold font-mono tracking-tight text-slate-900">
          {clampedScore.toFixed(1)}%
        </span>
        <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider mt-0.5">
          Mastitis Risk Score
        </p>
      </div>
    </div>
  );
};
