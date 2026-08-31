import React, { useState, useEffect } from 'react';
import { fetchAnimalsList } from '../services/api';
import { RiskBadge } from '../components/RiskBadge';
import { Search, Filter, ChevronLeft, ChevronRight, Eye } from 'lucide-react';

export const SurveillanceView = ({ onSelectAnimal }) => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState({ animals: [], total_count: 0, total_pages: 1 });
  const [page, setPage] = useState(1);
  const [pageSize] = useState(20);
  const [search, setSearch] = useState('');
  const [riskFilter, setRiskFilter] = useState('');
  const [breedFilter, setBreedFilter] = useState('');
  const [sortBy, setSortBy] = useState('animal_id');
  const [sortOrder, setSortOrder] = useState('asc');

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await fetchAnimalsList({
        page,
        page_size: pageSize,
        search: search.trim() || undefined,
        risk: riskFilter || undefined,
        breed: breedFilter || undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
      });
      setData(res);
    } catch (err) {
      console.error('Error fetching herd surveillance data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [page, search, riskFilter, breedFilter, sortBy, sortOrder]);

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('asc');
    }
  };

  return (
    <div className="space-y-6">
      {/* Search & Filter Header Toolbar */}
      <div className="bg-white border border-slate-200/90 rounded-2xl p-4 shadow-xs space-y-4">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          {/* Search Bar */}
          <div className="relative w-full md:w-80">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              placeholder="Search Animal ID or Farm ID..."
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
              className="w-full pl-9 pr-4 py-2 text-xs bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 font-medium"
            />
          </div>

          {/* Risk Level Filter Tabs */}
          <div className="flex items-center gap-1.5 flex-wrap">
            {[
              { id: '', label: 'All Herd' },
              { id: 'High', label: 'High Risk' },
              { id: 'Moderate', label: 'Moderate' },
              { id: 'Low', label: 'Low Risk' },
              { id: 'No_Risk', label: 'No Risk' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => {
                  setRiskFilter(tab.id);
                  setPage(1);
                }}
                className={`px-3 py-1.5 rounded-xl text-xs font-bold transition ${
                  riskFilter === tab.id
                    ? 'bg-slate-900 text-white shadow-xs'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Breed Dropdown Filter */}
          <div className="flex items-center gap-2 w-full md:w-auto">
            <Filter className="w-4 h-4 text-slate-400 shrink-0" />
            <select
              value={breedFilter}
              onChange={(e) => {
                setBreedFilter(e.target.value);
                setPage(1);
              }}
              className="px-3 py-1.5 text-xs font-medium bg-slate-50 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
            >
              <option value="">All Livestock Breeds</option>
              <option value="Holstein_Friesian">Holstein Friesian</option>
              <option value="Jersey_cross">Jersey Cross</option>
              <option value="Gir_cross">Gir Cross</option>
              <option value="Sahiwal_cross">Sahiwal Cross</option>
            </select>
          </div>
        </div>
      </div>

      {/* Surveillance Table Container */}
      <div className="bg-white border border-slate-200/90 rounded-2xl shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-500 border-b border-slate-200 font-bold uppercase tracking-wider text-[10px]">
              <tr>
                <th onClick={() => handleSort('animal_id')} className="p-3.5 cursor-pointer hover:text-slate-900">
                  Animal ID {sortBy === 'animal_id' && (sortOrder === 'asc' ? '↑' : '↓')}
                </th>
                <th className="p-3.5">Breed / Farm</th>
                <th onClick={() => handleSort('body_temperature_c')} className="p-3.5 cursor-pointer hover:text-slate-900">
                  Body Temp (°C) {sortBy === 'body_temperature_c' && (sortOrder === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('milk_conductivity_mS_cm')} className="p-3.5 cursor-pointer hover:text-slate-900">
                  Conductivity {sortBy === 'milk_conductivity_mS_cm' && (sortOrder === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('milk_yield_kg_day')} className="p-3.5 cursor-pointer hover:text-slate-900">
                  Yield (kg) {sortBy === 'milk_yield_kg_day' && (sortOrder === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('synthetic_risk_score_pct')} className="p-3.5 cursor-pointer hover:text-slate-900">
                  Risk Category & Score {sortBy === 'synthetic_risk_score_pct' && (sortOrder === 'asc' ? '↑' : '↓')}
                </th>
                <th className="p-3.5 text-right">Action</th>
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-100 font-medium">
              {loading ? (
                <tr>
                  <td colSpan={7} className="p-8 text-center text-slate-500">
                    <div className="inline-block animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-emerald-500 mr-2" />
                    Fetching herd records...
                  </td>
                </tr>
              ) : data.animals.length === 0 ? (
                <tr>
                  <td colSpan={7} className="p-8 text-center text-slate-500">
                    No livestock records found matching search filters.
                  </td>
                </tr>
              ) : (
                data.animals.map((cow) => (
                  <tr key={cow.animal_id} className="hover:bg-slate-50/80 transition">
                    <td className="p-3.5 font-bold font-mono text-slate-900">
                      #{cow.animal_id}
                    </td>
                    <td className="p-3.5">
                      <span className="font-semibold text-slate-800 block">{cow.breed}</span>
                      <span className="text-[10px] text-slate-500 font-mono">Farm: {cow.farm_id}</span>
                    </td>
                    <td className="p-3.5 font-mono text-slate-700">
                      {cow.body_temperature_c}°C
                    </td>
                    <td className="p-3.5 font-mono text-slate-700">
                      {cow.milk_conductivity_mS_cm} mS/cm
                    </td>
                    <td className="p-3.5 font-mono text-slate-700">
                      {cow.milk_yield_kg_day} kg
                    </td>
                    <td className="p-3.5">
                      <RiskBadge category={cow.mastitis_risk_category} score={cow.synthetic_risk_score_pct} size="sm" />
                    </td>
                    <td className="p-3.5 text-right">
                      <button
                        onClick={() => onSelectAnimal(cow.animal_id)}
                        className="px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-emerald-600 text-white font-bold text-xs flex items-center gap-1.5 ml-auto transition"
                      >
                        <Eye className="w-3.5 h-3.5" />
                        <span>Inspect</span>
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Footer */}
        <div className="p-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-xs text-slate-600 font-medium">
          <div>
            Showing <strong className="font-mono text-slate-900">{data.animals.length}</strong> of{' '}
            <strong className="font-mono text-slate-900">{data.total_count}</strong> total records
          </div>

          <div className="flex items-center gap-2">
            <button
              disabled={page <= 1}
              onClick={() => setPage(page - 1)}
              className="p-1.5 rounded-lg border bg-white hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="font-mono px-2 font-bold">
              Page {page} of {data.total_pages}
            </span>
            <button
              disabled={page >= data.total_pages}
              onClick={() => setPage(page + 1)}
              className="p-1.5 rounded-lg border bg-white hover:bg-slate-100 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
