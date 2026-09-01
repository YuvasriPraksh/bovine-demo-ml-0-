import React from 'react';
import { t } from '../utils/i18n';
import { speakText } from '../utils/tts';

export const FarmerDashboardView = ({ data, onSelectAnimal }) => {
  if (!data) {
    return (
      <div className="flex flex-col items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600"></div>
        <p className="mt-4 text-slate-500 font-medium">Loading your farm data...</p>
      </div>
    );
  }

  const handleAlertVoice = (cowId, isHighRisk) => {
    speakText(isHighRisk ? t('tts_abnormal_signals') : t('reason_watch'));
  };

  return (
    <div className="max-w-md mx-auto space-y-6 pb-20">
      {/* Greeting */}
      <div>
        <h1 className="text-2xl font-bold text-slate-900">{t('greeting')}</h1>
        <p className="text-sm text-slate-600 mt-1">{t('greeting_desc')}</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 gap-3">
        <div className="bg-white rounded-2xl p-4 shadow-sm border border-slate-100 flex flex-col items-center justify-center">
          <div className="text-3xl mb-1">🟢</div>
          <div className="text-2xl font-black text-slate-800">{data.stats.healthy_count}</div>
          <div className="text-xs font-bold text-slate-500 text-center uppercase tracking-wide">{t('healthy_cows')}</div>
        </div>
        <div className="bg-white rounded-2xl p-4 shadow-sm border border-slate-100 flex flex-col items-center justify-center">
          <div className="text-3xl mb-1">🔴</div>
          <div className="text-2xl font-black text-rose-600">{data.stats.critical_count + data.stats.needs_attention_count}</div>
          <div className="text-xs font-bold text-rose-500 text-center uppercase tracking-wide">{t('need_attention')}</div>
        </div>
      </div>

      {/* Attention Required List */}
      <div>
        <h2 className="text-lg font-bold text-slate-800 mb-3">{t('cows_need_attention')}</h2>
        
        {data.alerts.length === 0 ? (
          <div className="bg-emerald-50 rounded-xl p-4 text-center border border-emerald-100">
            <span className="text-2xl block mb-2">✨</span>
            <p className="text-emerald-800 font-medium">{t('no_alerts')}</p>
          </div>
        ) : (
          <div className="space-y-3">
            {data.alerts.slice(0, 5).map((alert, idx) => {
              const isHighRisk = alert.risk_level === 'High';
              return (
                <div key={idx} className={`bg-white rounded-2xl p-4 shadow-sm border ${isHighRisk ? 'border-rose-200' : 'border-amber-200'}`}>
                  <div className="flex justify-between items-start mb-2">
                    <div className="flex items-center gap-2">
                      <div className="text-2xl">{isHighRisk ? '🔴' : '🟡'}</div>
                      <div>
                        <h3 className="font-bold text-slate-900">{t('cow_id_prefix')}{alert.cow_id}</h3>
                        <p className={`text-xs font-bold ${isHighRisk ? 'text-rose-600' : 'text-amber-600'}`}>
                          {isHighRisk ? t('status_high_risk') : t('status_watch')}
                        </p>
                      </div>
                    </div>
                    <button 
                      onClick={() => handleAlertVoice(alert.cow_id, isHighRisk)}
                      className="p-2 bg-slate-100 text-slate-600 rounded-full hover:bg-slate-200"
                    >
                      🔊
                    </button>
                  </div>
                  
                  <p className="text-sm text-slate-600 mb-4">
                    {isHighRisk ? t('reason_abnormal') : t('reason_watch')}
                  </p>
                  
                  <button 
                    onClick={() => onSelectAnimal(alert.cow_id)}
                    className={`w-full py-2 rounded-xl text-sm font-bold transition ${
                      isHighRisk ? 'bg-rose-50 text-rose-700 hover:bg-rose-100' : 'bg-amber-50 text-amber-700 hover:bg-amber-100'
                    }`}
                  >
                    {t('view_cow')}
                  </button>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
