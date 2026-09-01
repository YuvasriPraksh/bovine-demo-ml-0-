import React, { useState, useEffect } from 'react';
import { ArrowLeft } from 'lucide-react';
import { t } from '../utils/i18n';
import { fetchAnimalDetail } from '../services/api';

export const CowDetailMobileView = ({ animalId, onClose }) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, [animalId]);

  const loadData = async () => {
    try {
      const result = await fetchAnimalDetail(animalId);
      setData(result);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !data) {
    return (
      <div className="fixed inset-0 z-50 bg-white flex flex-col items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-600"></div>
      </div>
    );
  }

  const { record, prediction } = data;
  
  // Map backend logic to UI
  const isHighRisk = prediction.risk_category === 'High' || prediction.mastitis_probability > 0.5;
  const isWatch = prediction.risk_category === 'Moderate';
  
  let icon = '🟢';
  let statusText = t('status_healthy');
  let bgClass = 'bg-emerald-50';
  let textClass = 'text-emerald-700';

  if (isHighRisk) {
    icon = '🔴';
    statusText = t('status_high_risk');
    bgClass = 'bg-rose-50';
    textClass = 'text-rose-700';
  } else if (isWatch) {
    icon = '🟡';
    statusText = t('status_watch');
    bgClass = 'bg-amber-50';
    textClass = 'text-amber-700';
  }

  // Interpret physiological signs very simply for the farmer
  const signs = [];
  if (record.Milk_Conductivity_mS_cm > 4.5) {
    signs.push({ icon: '🥛', label: t('milk_conductivity'), msg: t('higher_than_normal'), alert: true });
  }
  if (record.Udder_Temperature_C > 37.5) {
    signs.push({ icon: '🌡️', label: t('udder_temperature'), msg: t('higher_than_normal'), alert: true });
  }
  if (record.Rumination_Time_min < 450) {
    signs.push({ icon: '🐄', label: t('rumination'), msg: t('lower_than_normal'), alert: true });
  }
  if (record.Previous_Mastitis_History === 1) {
    signs.push({ icon: '📋', label: t('previous_mastitis'), msg: t('yes'), alert: true });
  }
  
  // If no abnormal signs but risk is high (edge case), just show general abnormal
  if (signs.length === 0 && (isHighRisk || isWatch)) {
      signs.push({ icon: '⚠️', label: t('reason_abnormal'), msg: '', alert: true });
  }

  return (
    <div className="fixed inset-0 z-50 bg-white flex flex-col md:hidden overflow-y-auto">
      {/* Top Bar */}
      <div className="sticky top-0 bg-white border-b border-slate-200 px-4 py-3 flex items-center shadow-sm">
        <button onClick={onClose} className="p-2 -ml-2 text-slate-500 active:bg-slate-100 rounded-full">
          <ArrowLeft className="w-6 h-6" />
        </button>
        <h2 className="text-lg font-bold text-slate-900 ml-2">{t('cow_id_prefix')}{animalId}</h2>
      </div>

      <div className="p-4 space-y-6 pb-24">
        {/* Large Status Card */}
        <div className={`rounded-2xl p-6 flex flex-col items-center justify-center border ${bgClass.replace('bg-', 'border-')}`}>
          <div className="text-6xl mb-2">{icon}</div>
          <h1 className={`text-2xl font-black ${textClass}`}>{statusText}</h1>
        </div>

        {/* Why are we concerned? (Only show if Watch or High Risk) */}
        {(isHighRisk || isWatch) && (
          <div>
            <h3 className="text-lg font-bold text-slate-900 mb-3">{t('why_concerned')}</h3>
            <div className="space-y-2">
              {signs.map((sign, idx) => (
                <div key={idx} className="flex items-center gap-3 bg-slate-50 p-3 rounded-xl border border-slate-100">
                  <div className="text-2xl">{sign.icon}</div>
                  <div>
                    <div className="font-bold text-slate-800 text-sm">{sign.label}</div>
                    <div className="text-rose-600 font-semibold text-xs flex items-center gap-1">
                      ⚠️ {sign.msg}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* What to do? */}
        {(isHighRisk || isWatch) && (
          <div>
            <h3 className="text-lg font-bold text-slate-900 mb-3">{t('what_to_do')}</h3>
            <div className="bg-blue-50 border border-blue-100 p-4 rounded-2xl">
              <ul className="space-y-3">
                <li className="flex gap-2 text-blue-900 font-medium text-sm">
                  <span>⚠️</span> {t('action_check_cow')}
                </li>
                {isHighRisk && (
                  <li className="flex gap-2 text-blue-900 font-medium text-sm">
                    <span>👨‍⚕️</span> {t('action_contact_vet')}
                  </li>
                )}
                <li className="flex gap-2 text-blue-900 font-medium text-sm">
                  <span>🐄</span> {t('action_follow_guidance')}
                </li>
              </ul>
            </div>
          </div>
        )}

        {/* Action Button */}
        {isHighRisk && (
          <button className="w-full py-4 bg-rose-600 active:bg-rose-700 text-white font-black text-lg rounded-2xl shadow-md transition flex justify-center items-center gap-2">
             👨‍⚕️ {t('btn_contact_vet')}
          </button>
        )}
      </div>
    </div>
  );
};
