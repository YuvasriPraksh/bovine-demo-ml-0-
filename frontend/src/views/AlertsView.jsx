import React, { useState, useEffect } from 'react';
import { fetchAnimalsList } from '../services/api';
import { ShieldCheck, Bell } from 'lucide-react';
import { t } from '../utils/i18n';
import { speakText } from '../utils/tts';

export const AlertsView = ({ onSelectAnimal }) => {
  const [loading, setLoading] = useState(true);
  const [highRiskCows, setHighRiskCows] = useState([]);

  const loadAlerts = async () => {
    setLoading(true);
    try {
      const res = await fetchAnimalsList({ risk: 'High', page_size: 15 });
      setHighRiskCows(res.animals || []);
    } catch (err) {
      console.error('Error fetching high risk alerts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAlerts();
  }, []);

  const handleAlertVoice = (cowId) => {
    speakText(t('tts_abnormal_signals'));
  };

  return (
    <div className="max-w-md mx-auto space-y-4 pb-20">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold text-slate-900">{t('nav_alerts')}</h1>
        <div className="bg-rose-100 text-rose-700 px-3 py-1 rounded-full text-xs font-bold">
          {highRiskCows.length} {t('nav_alerts')}
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600"></div>
        </div>
      ) : highRiskCows.length === 0 ? (
        <div className="bg-emerald-50 border border-emerald-100 rounded-2xl p-8 text-center mt-6">
          <ShieldCheck className="w-16 h-16 text-emerald-500 mx-auto mb-4" />
          <p className="font-bold text-emerald-800 text-lg mb-1">{t('no_alerts')}</p>
        </div>
      ) : (
        <div className="space-y-3">
          {highRiskCows.map((cow) => (
            <div
              key={cow.animal_id}
              onClick={() => onSelectAnimal(cow.animal_id)}
              className="bg-white rounded-2xl p-4 shadow-sm border border-rose-200 active:scale-95 transition cursor-pointer"
            >
              <div className="flex justify-between items-start mb-2">
                <div className="flex items-center gap-3">
                  <div className="text-3xl">🔴</div>
                  <div>
                    <h3 className="font-bold text-slate-900 text-lg">{t('cow_id_prefix')}{cow.animal_id}</h3>
                    <p className="text-sm font-bold text-rose-600">{t('status_high_risk')}</p>
                  </div>
                </div>
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    handleAlertVoice(cow.animal_id);
                  }}
                  className="p-2 bg-slate-100 text-slate-600 rounded-full hover:bg-slate-200"
                >
                  🔊
                </button>
              </div>
              
              <p className="text-slate-600 text-sm mb-3">
                {t('reason_abnormal')}
              </p>
              
              <div className="text-rose-600 text-sm font-bold flex items-center justify-end gap-1">
                <span>{t('view_cow')}</span>
                <span>›</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
