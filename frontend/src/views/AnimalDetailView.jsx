import React, { useState, useEffect } from 'react';
import { fetchAnimalDetail, fetchSensorData } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';
import { RiskGauge } from '../components/RiskGauge';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import {
  X,
  Thermometer,
  Activity,
  CheckCircle2,
  AlertTriangle,
  TrendingUp,
  FileText,
} from 'lucide-react';

export const AnimalDetailView = ({ animalId, onClose }) => {
  const [loading, setLoading] = useState(true);
  const [detail, setDetail] = useState(null);
  const [sensor, setSensor] = useState(null);

  const loadAllData = async () => {
    setLoading(true);
    try {
      const [detailRes, sensorRes] = await Promise.all([
        fetchAnimalDetail(animalId),
        fetchSensorData(animalId),
      ]);
      setDetail(detailRes);
      setSensor(sensorRes);
    } catch (err) {
      console.error('Error fetching animal detail:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (animalId) {
      loadAllData();
    }
  }, [animalId]);

  if (!animalId) return null;

  const cow = detail?.animal || {};
  const pred = detail?.prediction || {};
  const trend = sensor?.telemetry_trend || [];

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white border border-slate-200 rounded-2xl w-full max-w-4xl max-h-[90vh] overflow-y-auto shadow-2xl flex flex-col">
        {/* Modal Header */}
        <div className="p-5 border-b border-slate-200 flex items-center justify-between sticky top-0 bg-white z-10">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-emerald-100 border border-emerald-200 flex items-center justify-center font-bold text-emerald-800 text-sm font-mono">
              #{cow.animal_id || animalId}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="font-extrabold text-base text-slate-900">
                  Cow Profile #{cow.animal_id || animalId}
                </h3>
                <RiskBadge category={pred.risk_category} score={pred.risk_score} />
              </div>
              <p className="text-xs text-slate-500 font-medium">
                Breed: {cow.breed || 'Jersey Cross'} · Farm: {cow.farm_id || 'F16'} · Record Date: {cow.record_date || '2026-01-20'}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-2 rounded-xl text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        {loading ? (
          <div className="p-12 text-center text-slate-500">
            <div className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-emerald-500 mx-auto mb-2" />
            <span>Loading cow telemetry & AI risk report...</span>
          </div>
        ) : (
          <div className="p-6 space-y-6">
            {/* Risk Gauge & Summary Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center bg-slate-50/70 border border-slate-200/80 rounded-2xl p-4">
              <div className="md:col-span-1">
                <RiskGauge score={pred.risk_score} riskCategory={pred.risk_category} />
              </div>

              <div className="md:col-span-2 grid grid-cols-2 gap-4">
                <div className="p-3 bg-white border border-slate-200 rounded-xl">
                  <span className="text-[10px] uppercase font-semibold text-slate-400 block">Core Body Temp</span>
                  <span className="text-xl font-extrabold font-mono text-slate-900">{cow.body_temperature_c}°C</span>
                  <span className="text-[10px] text-slate-500 block mt-0.5">Ref Normal: ≤ 38.8°C</span>
                </div>
                <div className="p-3 bg-white border border-slate-200 rounded-xl">
                  <span className="text-[10px] uppercase font-semibold text-slate-400 block">Milk Conductivity</span>
                  <span className="text-xl font-extrabold font-mono text-slate-900">{cow.milk_conductivity_mS_cm} mS/cm</span>
                  <span className="text-[10px] text-slate-500 block mt-0.5">Ref Normal: ≤ 4.3 mS/cm</span>
                </div>
                <div className="p-3 bg-white border border-slate-200 rounded-xl">
                  <span className="text-[10px] uppercase font-semibold text-slate-400 block">Udder Surface Temp</span>
                  <span className="text-xl font-extrabold font-mono text-slate-900">{cow.udder_surface_temperature_c}°C</span>
                  <span className="text-[10px] text-slate-500 block mt-0.5">Ref Normal: ≤ 34.2°C</span>
                </div>
                <div className="p-3 bg-white border border-slate-200 rounded-xl">
                  <span className="text-[10px] uppercase font-semibold text-slate-400 block">Daily Milk Yield</span>
                  <span className="text-xl font-extrabold font-mono text-slate-900">{cow.milk_yield_kg_day} kg</span>
                  <span className="text-[10px] text-slate-500 block mt-0.5">Ref Normal: ≥ 15.0 kg</span>
                </div>
              </div>
            </div>

            {/* 7-Day Telemetry Trend Chart */}
            <div className="bg-white border border-slate-200/90 rounded-2xl p-4 shadow-xs">
              <div className="flex items-center justify-between mb-3">
                <div>
                  <h4 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider">
                    7-Day Historical Sensor Trend
                  </h4>
                  <p className="text-[11px] text-slate-500 font-medium">
                    Continuous conductivity & temperature drift over past week
                  </p>
                </div>
                <TrendingUp className="w-4 h-4 text-emerald-600" />
              </div>
              <div className="h-52">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={trend} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <defs>
                      <linearGradient id="condGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.4} />
                        <stop offset="95%" stopColor="#f43f5e" stopOpacity={0.0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                    <XAxis dataKey="day" stroke="#64748b" tick={{ fontSize: 10 }} />
                    <YAxis stroke="#64748b" tick={{ fontSize: 10 }} />
                    <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '12px' }} />
                    <Area type="monotone" dataKey="milk_conductivity_mS_cm" name="Conductivity (mS/cm)" stroke="#f43f5e" fillOpacity={1} fill="url(#condGrad)" strokeWidth={2} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Explainable Risk Factors & Recommendations */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Risk Factors */}
              <div className="bg-slate-50 border border-slate-200 rounded-2xl p-4 space-y-3">
                <h4 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                  <AlertTriangle className="w-4 h-4 text-amber-500" />
                  <span>Explainable AI: Model Risk Factors</span>
                </h4>
                <div className="space-y-2">
                  {(pred.top_risk_factors || []).map((f, i) => (
                    <div key={i} className="p-2.5 bg-white border border-slate-200 rounded-xl text-xs flex items-center justify-between">
                      <div>
                        <span className="font-bold text-slate-800 block">{f.factor}</span>
                        <span className="text-[10px] text-slate-500 font-mono">{f.details}</span>
                      </div>
                      <span className="font-mono font-extrabold text-amber-600 text-xs">
                        +{f.impact_score}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommendations */}
              <div className="bg-emerald-50/50 border border-emerald-100 rounded-2xl p-4 space-y-3">
                <h4 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                  <FileText className="w-4 h-4 text-emerald-600" />
                  <span>Veterinary Clinical Action Plan</span>
                </h4>
                <ul className="space-y-2 text-xs text-slate-700 font-medium">
                  {(pred.recommendations || []).map((rec, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                      <span>{rec}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
