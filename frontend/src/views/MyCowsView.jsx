import React, { useState, useEffect } from 'react';
import { Search } from 'lucide-react';
import { t } from '../utils/i18n';
import { fetchAnimalsList } from '../services/api';

export const MyCowsView = ({ onSelectAnimal }) => {
  const [cows, setCows] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadCows();
  }, []);

  const loadCows = async () => {
    try {
      const res = await fetchAnimalsList({ page_size: 100 });
      setCows(res.animals || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredCows = cows.filter(c => 
    c.animal_id && c.animal_id.toString().includes(searchTerm)
  );

  if (loading) {
    return (
      <div className="flex justify-center py-12">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-md mx-auto pb-20">
      <h1 className="text-2xl font-bold text-slate-900 mb-4">{t('nav_my_cows')}</h1>
      
      <div className="relative mb-6">
        <Search className="w-5 h-5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
        <input
          type="text"
          placeholder={t('search_placeholder')}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-3 bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 shadow-sm"
        />
      </div>

      <div className="space-y-3">
        {filteredCows.map(cow => {
          const isHighRisk = cow.mastitis_risk_category === 'High';
          const isWatch = cow.mastitis_risk_category === 'Moderate';
          
          let icon = '🟢';
          let statusText = t('status_healthy');
          let borderColor = 'border-slate-100';

          if (isHighRisk) {
            icon = '🔴';
            statusText = t('status_high_risk');
            borderColor = 'border-rose-200';
          } else if (isWatch) {
            icon = '🟡';
            statusText = t('status_watch');
            borderColor = 'border-amber-200';
          }

          return (
            <div 
              key={cow.animal_id} 
              onClick={() => onSelectAnimal(cow.animal_id)}
              className={`bg-white rounded-xl p-4 shadow-sm border ${borderColor} flex items-center justify-between active:scale-95 transition cursor-pointer`}
            >
              <div className="flex items-center gap-3">
                <div className="text-3xl">{icon}</div>
                <div>
                  <h3 className="font-bold text-slate-900 text-lg">{t('cow_id_prefix')}{cow.animal_id}</h3>
                  <p className={`text-sm font-medium ${isHighRisk ? 'text-rose-600' : isWatch ? 'text-amber-600' : 'text-emerald-600'}`}>
                    {statusText}
                  </p>
                </div>
              </div>
              <div className="text-slate-400">›</div>
            </div>
          );
        })}
        {filteredCows.length === 0 && (
          <p className="text-center text-slate-500 py-4">No cows found.</p>
        )}
      </div>
    </div>
  );
};
