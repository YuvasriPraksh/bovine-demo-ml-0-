import React from 'react';
import {
  PieChart as RePieChart,
  Pie,
  Cell,
  BarChart as ReBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import { StatCard } from '../components/StatCard';
import { RiskBadge } from '../components/RiskBadge';
import {
  Users,
  ShieldCheck,
  AlertTriangle,
  Flame,
  Thermometer,
  Activity,
  ArrowRight,
  TrendingUp,
  CloudSun,
} from 'lucide-react';

export const DashboardView = ({ data, onSelectAnimal, onNavigate }) => {
  if (!data) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-emerald-500" />
      </div>
    );
  }

  const riskPieData = [
    { name: 'No Risk', value: data.no_risk_count, color: '#10b981' },
    { name: 'Low Risk', value: data.low_risk_count, color: '#0ea5e9' },
    { name: 'Moderate Risk', value: data.moderate_risk_count, color: '#f59e0b' },
    { name: 'High Risk Alert', value: data.high_risk_count, color: '#f43f5e' },
  ];

  const sensorBarData = [
    { metric: 'Body Temp (°C)', value: data.herd_averages.avg_body_temp, normal: 38.6 },
    { metric: 'Udder Temp (°C)', value: data.herd_averages.avg_udder_temp, normal: 33.8 },
    { metric: 'Conductivity', value: data.herd_averages.avg_milk_conductivity, normal: 4.2 },
    { metric: 'Milk Yield (kg)', value: data.herd_averages.avg_milk_yield, normal: 15.0 },
    { metric: 'Hygiene Score', value: data.herd_averages.avg_hygiene_score, normal: 65.0 },
  ];

  const env = data.environmental_status || {};

  return (
    <div className="space-y-6">
      {/* First Viewport: Key Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        <StatCard
          title="Total Herd"
          value={data.total_animals.toLocaleString()}
          subtext="Direct Excel/CSV Data Source"
          icon={Users}
          color="slate"
        />
        <StatCard
          title="No Risk"
          value={data.no_risk_count.toLocaleString()}
          subtext={`${data.risk_distribution_pct.No_Risk}% Healthy Herd`}
          icon={ShieldCheck}
          color="emerald"
        />
        <StatCard
          title="Low Risk"
          value={data.low_risk_count.toLocaleString()}
          subtext={`${data.risk_distribution_pct.Low}% Routine Monitoring`}
          icon={Activity}
          color="sky"
        />
        <StatCard
          title="Moderate Risk"
          value={data.moderate_risk_count.toLocaleString()}
          subtext={`${data.risk_distribution_pct.Moderate}% Subclinical Drift`}
          icon={Flame}
          color="amber"
        />
        <StatCard
          title="High Risk Alert"
          value={data.high_risk_count.toLocaleString()}
          subtext={`${data.risk_distribution_pct.High}% Critical Attention`}
          icon={AlertTriangle}
          color="rose"
        />
      </div>

      {/* Main Charts & Environmental Widgets */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Distribution Pie Chart */}
        <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-xs">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h3 className="text-sm font-extrabold text-slate-900">
                Herd Risk Distribution
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                XGBoost Multi-Class Segmentation
              </p>
            </div>
            <Activity className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <RePieChart>
                <Pie
                  data={riskPieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={80}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {riskPieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#ffffff',
                    borderColor: '#e2e8f0',
                    borderRadius: '12px',
                    boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)',
                  }}
                  itemStyle={{ color: '#0f172a', fontWeight: 'bold' }}
                />
              </RePieChart>
            </ResponsiveContainer>
          </div>
          <div className="grid grid-cols-2 gap-2 mt-1">
            {riskPieData.map((item) => (
              <div key={item.name} className="flex items-center gap-2 text-xs font-medium text-slate-600">
                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: item.color }} />
                <span>{item.name}: <strong className="font-mono text-slate-900">{item.value}</strong></span>
              </div>
            ))}
          </div>
        </div>

        {/* Herd Sensor Means Bar Chart */}
        <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-xs">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h3 className="text-sm font-extrabold text-slate-900">
                Herd Biometric Means
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                Observed Mean vs Normal Reference Baselines
              </p>
            </div>
            <Thermometer className="w-4 h-4 text-sky-600" />
          </div>
          <div className="h-60">
            <ResponsiveContainer width="100%" height="100%">
              <ReBarChart data={sensorBarData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="metric" stroke="#64748b" tick={{ fontSize: 9 }} interval={0} angle={-15} textAnchor="end" />
                <YAxis stroke="#64748b" tick={{ fontSize: 10 }} />
                <Tooltip contentStyle={{ backgroundColor: '#ffffff', borderColor: '#e2e8f0', borderRadius: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Bar dataKey="value" name="Herd Average" fill="#0ea5e9" radius={[4, 4, 0, 0]} />
                <Bar dataKey="normal" name="Normal Baseline" fill="#10b981" radius={[4, 4, 0, 0]} />
              </ReBarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Environmental Heat Stress THI Widget */}
        <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3">
              <div>
                <h3 className="text-sm font-extrabold text-slate-900">
                  Barn Microclimate (THI)
                </h3>
                <p className="text-xs text-slate-500 font-medium">
                  Temperature Humidity Index
                </p>
              </div>
              <CloudSun className="w-5 h-5 text-amber-500" />
            </div>

            <div className="p-4 rounded-xl bg-amber-50/60 border border-amber-100 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-600">Calculated THI Index</span>
                <span className="text-xl font-extrabold font-mono text-amber-700">
                  {env.calculated_thi || 76.5}
                </span>
              </div>
              <div className="grid grid-cols-2 gap-2 text-xs pt-2 border-t border-amber-200/60">
                <div>
                  <span className="text-slate-500 block text-[10px]">Ambient Temp</span>
                  <span className="font-mono font-bold text-slate-800">{env.ambient_temperature_c || 28.5}°C</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px]">Barn Humidity</span>
                  <span className="font-mono font-bold text-slate-800">{env.relative_humidity_pct || 72.0}%</span>
                </div>
              </div>
            </div>

            <p className="text-xs font-medium text-slate-600 mt-3">
              {env.interpretation || 'Elevated THI associates with increased bacterial proliferation in bedding.'}
            </p>
          </div>

          <button
            onClick={() => onNavigate('predictor')}
            className="w-full mt-4 py-2 px-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs flex items-center justify-center gap-2 transition"
          >
            <span>Run Custom AI Prediction</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Critical High-Risk Alert Feed & Live Telemetry Table */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Decision Support Alerts */}
        <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-extrabold text-slate-900">
                Critical Decision-Support Alerts
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                Cows flagged for immediate California Mastitis Test (CMT) screening
              </p>
            </div>
            <button
              onClick={() => onNavigate('alerts')}
              className="text-xs font-bold text-emerald-600 hover:text-emerald-700 flex items-center gap-1"
            >
              <span>View All</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="space-y-3">
            {(data.recent_high_risk_alerts || []).slice(0, 4).map((alert) => (
              <div
                key={alert.animal_id}
                onClick={() => onSelectAnimal(alert.animal_id)}
                className="p-3.5 rounded-xl bg-rose-50/50 border border-rose-100 hover:border-rose-300 cursor-pointer transition flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-rose-100 border border-rose-200 flex items-center justify-center text-rose-700 font-bold text-xs font-mono">
                    #{alert.animal_id}
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-slate-900">{alert.breed}</span>
                      <span className="text-[10px] text-slate-500 font-mono">Farm: {alert.farm_id}</span>
                    </div>
                    <div className="flex items-center gap-1.5 mt-1 flex-wrap">
                      {(alert.top_factors || []).map((factor, idx) => (
                        <span
                          key={idx}
                          className="text-[10px] px-1.5 py-0.5 rounded bg-white text-rose-700 font-medium border border-rose-200"
                        >
                          {factor}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-sm font-black font-mono text-rose-600">
                    {alert.risk_score}%
                  </span>
                  <p className="text-[10px] text-rose-600 uppercase font-bold">HIGH RISK</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Live Herd Telemetry Stream */}
        <div className="bg-white border border-slate-200/90 rounded-2xl p-5 shadow-xs">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-extrabold text-slate-900">
                Recent Herd Telemetry Stream
              </h3>
              <p className="text-xs text-slate-500 font-medium">
                Live observations from dataset stream
              </p>
            </div>
            <button
              onClick={() => onNavigate('surveillance')}
              className="text-xs font-bold text-emerald-600 hover:text-emerald-700 flex items-center gap-1"
            >
              <span>Explore Herd</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="text-slate-500 border-b border-slate-200 font-semibold">
                <tr>
                  <th className="pb-2">Animal</th>
                  <th className="pb-2">Breed</th>
                  <th className="pb-2">Conductivity</th>
                  <th className="pb-2">Body Temp</th>
                  <th className="pb-2">Risk</th>
                  <th className="pb-2 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {(data.recent_predictions || []).slice(0, 5).map((cow) => (
                  <tr key={cow.animal_id} className="hover:bg-slate-50 transition">
                    <td className="py-2.5 font-bold text-slate-900 font-mono">#{cow.animal_id}</td>
                    <td className="py-2.5 text-slate-600 font-medium">{cow.breed}</td>
                    <td className="py-2.5 font-mono text-slate-700">{cow.milk_conductivity_mS_cm} mS/cm</td>
                    <td className="py-2.5 font-mono text-slate-700">{cow.body_temperature_c} °C</td>
                    <td className="py-2.5">
                      <RiskBadge category={cow.mastitis_risk_category} score={cow.synthetic_risk_score_pct} size="sm" />
                    </td>
                    <td className="py-2.5 text-right">
                      <button
                        onClick={() => onSelectAnimal(cow.animal_id)}
                        className="px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-emerald-600 hover:text-white text-slate-700 transition text-[11px] font-bold"
                      >
                        Inspect
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};
