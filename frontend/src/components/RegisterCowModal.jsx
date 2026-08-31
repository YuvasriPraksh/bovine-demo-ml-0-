import React, { useState } from 'react';
import { registerCow } from '../services/api';
import { X, PlusCircle, CheckCircle2, AlertTriangle } from 'lucide-react';

export const RegisterCowModal = ({ onClose, onSuccess }) => {
  const [form, setForm] = useState({
    animal_id: Math.floor(12000 + Math.random() * 8000),
    farm_id: 'F16',
    breed: 'Gir_cross',
    age_years: 4.5,
    lactation_number: 3,
    days_in_milk: 60,
    body_temperature_c: 38.6,
    udder_surface_temperature_c: 33.8,
    milk_conductivity_mS_cm: 4.2,
    milk_yield_kg_day: 16.5,
    previous_mastitis_history: 0,
    vaccinated: 1,
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === 'number' ? (value === '' ? '' : parseFloat(value)) : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const res = await registerCow(form);
      if (onSuccess) onSuccess(res);
      onClose();
    } catch (err) {
      console.error('Cow Registration Error:', err);
      setError(err.response?.data?.detail || 'Error registering cow.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white border border-slate-200 rounded-2xl w-full max-w-xl shadow-2xl p-6 space-y-5">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2">
            <PlusCircle className="w-5 h-5 text-emerald-600" />
            <h3 className="text-base font-extrabold text-slate-900">
              Register New Cow Record
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {error && (
          <div className="p-3 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs font-semibold flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">Animal Tag ID</label>
              <input
                type="number"
                name="animal_id"
                required
                value={form.animal_id}
                onChange={handleChange}
                className="w-full px-3 py-1.5 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl"
              />
            </div>
            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">Farm Station ID</label>
              <input
                type="text"
                name="farm_id"
                required
                value={form.farm_id}
                onChange={handleChange}
                className="w-full px-3 py-1.5 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">Livestock Breed</label>
              <select
                name="breed"
                value={form.breed}
                onChange={handleChange}
                className="w-full px-3 py-1.5 text-xs font-medium bg-slate-50 border border-slate-200 rounded-xl"
              >
                <option value="Holstein_Friesian">Holstein Friesian</option>
                <option value="Jersey_cross">Jersey Cross</option>
                <option value="Gir_cross">Gir Cross</option>
                <option value="Sahiwal_cross">Sahiwal Cross</option>
              </select>
            </div>
            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">Age (Years)</label>
              <input
                type="number"
                step="0.1"
                name="age_years"
                value={form.age_years}
                onChange={handleChange}
                className="w-full px-3 py-1.5 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">Milk Conductivity (mS/cm)</label>
              <input
                type="number"
                step="0.1"
                name="milk_conductivity_mS_cm"
                value={form.milk_conductivity_mS_cm}
                onChange={handleChange}
                className="w-full px-3 py-1.5 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl"
              />
            </div>
            <div>
              <label className="text-xs font-bold text-slate-700 block mb-1">Body Temperature (°C)</label>
              <input
                type="number"
                step="0.1"
                name="body_temperature_c"
                value={form.body_temperature_c}
                onChange={handleChange}
                className="w-full px-3 py-1.5 text-xs font-mono bg-slate-50 border border-slate-200 rounded-xl"
              />
            </div>
          </div>

          <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-100">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 rounded-xl text-xs font-bold text-slate-600 bg-slate-100 hover:bg-slate-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 rounded-xl bg-slate-900 hover:bg-emerald-600 text-white font-bold text-xs flex items-center gap-1.5"
            >
              {loading ? 'Saving Record...' : 'Register Animal'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
