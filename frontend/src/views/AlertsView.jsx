import React, { useState, useEffect } from 'react';
import { fetchAnimalsList } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';
import { AlertTriangle, CheckCircle2, ShieldCheck, Eye, FileText, Activity } from 'lucide-react';

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

  const sops = [
    {
      step: '1. On-Farm CMT Screening',
      detail: 'Conduct California Mastitis Test (CMT) or single-quarter electrical conductivity test during next milking session.',
    },
    {
      step: '2. Milk Isolation Protocol',
      detail: 'Isolate milk from flagged quarters into separate buckets. Do NOT mix into main bulk tank until subclinical clear.',
    },
    {
      step: '3. Teat Hygiene & Pre-Dip',
      detail: 'Inspect teat end integrity. Ensure full 30-second pre-dip contact time and barrier post-dip application.',
    },
    {
      step: '4. Barn Bedding Management',
      detail: 'If barn THI > 72, replace wet stall bedding daily to reduce environmental pathogen proliferation (S. uberis, E. coli).',
    },
  ];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
      {/* High-Risk Alerts Feed Column */}
      <div className="lg:col-span-7 bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs space-y-4">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div>
            <h3 className="text-base font-extrabold text-slate-900 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-rose-500" />
              <span>High-Risk Livestock Decision Alerts</span>
            </h3>
            <p className="text-xs text-slate-500 font-medium mt-0.5">
              Cows requiring immediate veterinary inspection or CMT quarter screening
            </p>
          </div>
          <span className="px-2.5 py-1 rounded-full bg-rose-50 text-rose-700 border border-rose-200 text-xs font-bold font-mono">
            {highRiskCows.length} Active Alerts
          </span>
        </div>

        {loading ? (
          <div className="p-8 text-center text-slate-500">
            <div className="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-emerald-500 mx-auto mb-2" />
            <span>Loading active alerts...</span>
          </div>
        ) : highRiskCows.length === 0 ? (
          <div className="p-8 text-center text-slate-500">
            <ShieldCheck className="w-10 h-10 text-emerald-500 mx-auto mb-2" />
            <p className="font-bold text-slate-800">No High-Risk Alerts Active</p>
            <p className="text-xs text-slate-500">All monitored cows currently register within healthy parameters.</p>
          </div>
        ) : (
          <div className="space-y-3">
            {highRiskCows.map((cow) => (
              <div
                key={cow.animal_id}
                className="p-4 rounded-xl bg-rose-50/40 border border-rose-100 hover:border-rose-300 transition flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-rose-100 border border-rose-200 flex items-center justify-center font-extrabold font-mono text-rose-800 text-xs">
                    #{cow.animal_id}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-slate-900 text-xs">{cow.breed}</span>
                      <span className="text-[10px] text-slate-500 font-mono">Farm: {cow.farm_id}</span>
                    </div>
                    <div className="flex items-center gap-3 text-xs text-slate-600 mt-1 font-mono">
                      <span>Body: <strong className="text-slate-900">{cow.body_temperature_c}°C</strong></span>
                      <span>Cond: <strong className="text-slate-900">{cow.milk_conductivity_mS_cm} mS/cm</strong></span>
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  <RiskBadge category={cow.mastitis_risk_category} score={cow.synthetic_risk_score_pct} />
                  <button
                    onClick={() => onSelectAnimal(cow.animal_id)}
                    className="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-emerald-600 text-white font-bold text-xs flex items-center gap-1 transition"
                  >
                    <Eye className="w-3.5 h-3.5" />
                    <span>Inspect</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Recommended Veterinary SOP Action Guidelines */}
      <div className="lg:col-span-5 bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs space-y-4 flex flex-col justify-between">
        <div>
          <div className="flex items-center justify-between border-b border-slate-100 pb-3 mb-4">
            <div>
              <h3 className="text-sm font-extrabold text-slate-900 flex items-center gap-2">
                <FileText className="w-4 h-4 text-emerald-600" />
                <span>Standard Veterinary Action SOP</span>
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                Protocol for subclinical mastitis early intervention
              </p>
            </div>
          </div>

          <div className="space-y-3">
            {sops.map((sop, idx) => (
              <div key={idx} className="p-3.5 rounded-xl bg-slate-50 border border-slate-200/80 space-y-1">
                <h4 className="text-xs font-extrabold text-slate-900">{sop.step}</h4>
                <p className="text-xs text-slate-600 font-medium leading-relaxed">{sop.detail}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-800 font-medium">
          <p className="font-bold mb-0.5">Decision-Support Notice:</p>
          These protocols assist dairy operators and veterinary personnel in preventing clinical mastitis progression. Always consult registered veterinary officers for pharmaceutical administration.
        </div>
      </div>
    </div>
  );
};
