import React, { useState } from 'react';
import { runPredict } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';
import { RiskGauge } from '../components/RiskGauge';
import {
  Cpu,
  Thermometer,
  Activity,
  CloudSun,
  ShieldAlert,
  CheckCircle2,
  AlertTriangle,
  Play,
  RotateCcw,
  Sparkles,
} from 'lucide-react';

export const PredictorView = () => {
  const defaultForm = {
    animal_id: 'COW_LIVE_TEST_12001',
    breed: 'Holstein_Friesian',
    age_years: 4.5,
    lactation_number: 3,
    days_in_milk: 75,
    previous_mastitis_history: 1,
    vaccinated: 1,
    chronic_disease_flag: 0,

    body_temperature_c: 39.6,
    udder_surface_temperature_c: 39.2,

    milk_yield_kg_day: 12.0,
    milk_conductivity_mS_cm: 5.4,

    activity_score: 45.0,
    rumination_min_day: 350.0,
    feed_intake_kg_day: 14.5,
    water_intake_l_day: 60.0,

    ambient_temperature_c: 32.0,
    relative_humidity_pct: 80.0,
    hygiene_score_0_100: 45.0,
    dominant_environment_pathogen: 'S_uberis',
  };

  const [form, setForm] = useState(defaultForm);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === 'number' ? (value === '' ? '' : parseFloat(value)) : value,
    }));
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await runPredict(form);
      setResult(res);
    } catch (err) {
      console.error('Prediction API Error:', err);
      setError(err.response?.data?.detail || 'Error connecting to ML backend service.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
      {/* Form Controls Column */}
      <div className="lg:col-span-7 bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs space-y-6">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div>
            <h3 className="text-base font-extrabold text-slate-900 flex items-center gap-2">
              <Cpu className="w-5 h-5 text-emerald-600" />
              <span>Live IoT Telemetry & Sensor Console</span>
            </h3>
            <p className="text-xs text-slate-500 font-medium mt-0.5">
              Enter or adjust sensor measurements for instant 23-factor XGBoost risk prediction
            </p>
          </div>
          <button
            type="button"
            onClick={() => setForm(defaultForm)}
            className="px-3 py-1.5 rounded-xl text-xs font-bold text-slate-600 bg-slate-100 hover:bg-slate-200 flex items-center gap-1.5 transition"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset Demo</span>
          </button>
        </div>

        <form onSubmit={handlePredict} className="space-y-6">
          {/* Section 1: Milking Vitals */}
          <div>
            <h4 className="text-xs font-extrabold text-slate-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <span>🥛 Milking Vitals & Quality</span>
            </h4>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-semibold text-slate-600 block mb-1">
                  Milk Conductivity (mS/cm)
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="milk_conductivity_mS_cm"
                  value={form.milk_conductivity_mS_cm}
                  onChange={handleChange}
                  className="w-full px-3 py-2 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20"
                />
                <span className="text-[10px] text-slate-400">Normal: ≤ 4.3 mS/cm</span>
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-600 block mb-1">
                  Daily Milk Yield (kg/day)
                </label>
                <input
                  type="number"
                  step="0.5"
                  name="milk_yield_kg_day"
                  value={form.milk_yield_kg_day}
                  onChange={handleChange}
                  className="w-full px-3 py-2 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20"
                />
                <span className="text-[10px] text-slate-400">Normal: ≥ 15.0 kg</span>
              </div>
            </div>
          </div>

          {/* Section 2: Biometric Temperatures */}
          <div>
            <h4 className="text-xs font-extrabold text-slate-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <Thermometer className="w-4 h-4 text-rose-500" />
              <span>Biometric Temperature Sensors</span>
            </h4>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-xs font-semibold text-slate-600 block mb-1">
                  Core Body Temperature (°C)
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="body_temperature_c"
                  value={form.body_temperature_c}
                  onChange={handleChange}
                  className="w-full px-3 py-2 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20"
                />
                <span className="text-[10px] text-slate-400">Normal: 38.0 - 38.8°C</span>
              </div>
              <div>
                <label className="text-xs font-semibold text-slate-600 block mb-1">
                  Udder Surface Temp (°C)
                </label>
                <input
                  type="number"
                  step="0.1"
                  name="udder_surface_temperature_c"
                  value={form.udder_surface_temperature_c}
                  onChange={handleChange}
                  className="w-full px-3 py-2 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-emerald-500/20"
                />
                <span className="text-[10px] text-slate-400">Normal: 33.0 - 34.2°C</span>
              </div>
            </div>
          </div>

          {/* Section 3: Behavior & Nutrition */}
          <div>
            <h4 className="text-xs font-extrabold text-slate-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <Activity className="w-4 h-4 text-sky-500" />
              <span>Behavior & Intake Telemetry</span>
            </h4>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              <div>
                <label className="text-[11px] font-semibold text-slate-600 block mb-1">Activity Score</label>
                <input
                  type="number"
                  name="activity_score"
                  value={form.activity_score}
                  onChange={handleChange}
                  className="w-full px-2.5 py-1.5 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl"
                />
              </div>
              <div>
                <label className="text-[11px] font-semibold text-slate-600 block mb-1">Rumination (min)</label>
                <input
                  type="number"
                  name="rumination_min_day"
                  value={form.rumination_min_day}
                  onChange={handleChange}
                  className="w-full px-2.5 py-1.5 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl"
                />
              </div>
              <div>
                <label className="text-[11px] font-semibold text-slate-600 block mb-1">Feed Intake (kgDM)</label>
                <input
                  type="number"
                  name="feed_intake_kg_day"
                  value={form.feed_intake_kg_day}
                  onChange={handleChange}
                  className="w-full px-2.5 py-1.5 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl"
                />
              </div>
              <div>
                <label className="text-[11px] font-semibold text-slate-600 block mb-1">Water Intake (L)</label>
                <input
                  type="number"
                  name="water_intake_l_day"
                  value={form.water_intake_l_day}
                  onChange={handleChange}
                  className="w-full px-2.5 py-1.5 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl"
                />
              </div>
            </div>
          </div>

          {/* Section 4: Environment & Hygiene */}
          <div>
            <h4 className="text-xs font-extrabold text-slate-700 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <CloudSun className="w-4 h-4 text-amber-500" />
              <span>Environment & Microclimate</span>
            </h4>
            <div className="grid grid-cols-3 gap-3">
              <div>
                <label className="text-[11px] font-semibold text-slate-600 block mb-1">Ambient Temp (°C)</label>
                <input
                  type="number"
                  name="ambient_temperature_c"
                  value={form.ambient_temperature_c}
                  onChange={handleChange}
                  className="w-full px-2.5 py-1.5 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl"
                />
              </div>
              <div>
                <label className="text-[11px] font-semibold text-slate-600 block mb-1">Humidity (%)</label>
                <input
                  type="number"
                  name="relative_humidity_pct"
                  value={form.relative_humidity_pct}
                  onChange={handleChange}
                  className="w-full px-2.5 py-1.5 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl"
                />
              </div>
              <div>
                <label className="text-[11px] font-semibold text-slate-600 block mb-1">Hygiene Score (0-100)</label>
                <input
                  type="number"
                  name="hygiene_score_0_100"
                  value={form.hygiene_score_0_100}
                  onChange={handleChange}
                  className="w-full px-2.5 py-1.5 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl"
                />
              </div>
            </div>
          </div>

          {/* Section 5: Animal Profile */}
          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="text-[11px] font-semibold text-slate-600 block mb-1">Breed</label>
              <select
                name="breed"
                value={form.breed}
                onChange={handleChange}
                className="w-full px-2.5 py-1.5 text-xs font-medium bg-slate-50 border border-slate-200 rounded-xl"
              >
                <option value="Holstein_Friesian">Holstein Friesian</option>
                <option value="Jersey_cross">Jersey Cross</option>
                <option value="Gir_cross">Gir Cross</option>
                <option value="Sahiwal_cross">Sahiwal Cross</option>
              </select>
            </div>
            <div>
              <label className="text-[11px] font-semibold text-slate-600 block mb-1">Past Mastitis History</label>
              <select
                name="previous_mastitis_history"
                value={form.previous_mastitis_history}
                onChange={handleChange}
                className="w-full px-2.5 py-1.5 text-xs font-medium bg-slate-50 border border-slate-200 rounded-xl"
              >
                <option value={1}>Yes (Prior Episode)</option>
                <option value={0}>No History</option>
              </select>
            </div>
            <div>
              <label className="text-[11px] font-semibold text-slate-600 block mb-1">Vaccinated</label>
              <select
                name="vaccinated"
                value={form.vaccinated}
                onChange={handleChange}
                className="w-full px-2.5 py-1.5 text-xs font-medium bg-slate-50 border border-slate-200 rounded-xl"
              >
                <option value={1}>Yes (Protected)</option>
                <option value={0}>Unvaccinated</option>
              </select>
            </div>
          </div>

          {/* Run AI Prediction CTA Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-extrabold text-sm shadow-md shadow-emerald-500/20 transition flex items-center justify-center gap-2 disabled:opacity-50"
          >
            {loading ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white" />
                <span>Processing XGBoost Model Inference...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Run AI Mastitis Prediction Engine</span>
              </>
            )}
          </button>
        </form>
      </div>

      {/* Results Display Column */}
      <div className="lg:col-span-5 space-y-6">
        {error && (
          <div className="p-4 rounded-2xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-semibold flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {!result && !error && (
          <div className="bg-white border border-slate-200/90 rounded-2xl p-8 shadow-xs text-center space-y-3">
            <div className="w-12 h-12 rounded-2xl bg-emerald-50 border border-emerald-100 flex items-center justify-center text-emerald-600 mx-auto">
              <Cpu className="w-6 h-6" />
            </div>
            <h4 className="font-extrabold text-slate-900 text-base">
              Ready for AI Analysis
            </h4>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">
              Adjust sensor parameters on the left and click "Run AI Mastitis Prediction Engine" to generate real-time XGBoost risk predictions.
            </p>
          </div>
        )}

        {result && (
          <div className="bg-white border border-slate-200/90 rounded-2xl p-6 shadow-xs space-y-5">
            {/* Header Status */}
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div>
                <span className="text-[10px] uppercase font-mono font-bold text-slate-400 block">
                  Prediction Output ID #{result.animal_id}
                </span>
                <h4 className="text-base font-extrabold text-slate-900">
                  {result.risk_label || 'AI Disease Forecast'}
                </h4>
              </div>
              <RiskBadge category={result.risk_category} score={result.risk_score} />
            </div>

            {/* Semicircular SVG Risk Gauge */}
            <RiskGauge score={result.risk_score} riskCategory={result.risk_category} />

            {/* Model-Derived Top Risk Factors */}
            <div>
              <h5 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider mb-2.5">
                Explainable AI: Model Risk Factors
              </h5>
              <div className="space-y-2">
                {(result.top_risk_factors || []).map((f, i) => (
                  <div
                    key={i}
                    className="p-2.5 rounded-xl bg-slate-50 border border-slate-200/80 flex items-center justify-between text-xs"
                  >
                    <div>
                      <span className="font-bold text-slate-800 block">{f.factor}</span>
                      <span className="text-[10px] text-slate-500 font-mono">{f.details}</span>
                    </div>
                    <span className="font-mono font-extrabold text-rose-600 text-xs">
                      +{f.impact_score}
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Clinical Recommendations */}
            <div>
              <h5 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider mb-2">
                Veterinary Decision Support Actions
              </h5>
              <ul className="space-y-1.5 text-xs text-slate-600 font-medium">
                {(result.recommendations || []).map((rec, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                    <span>{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
