import React from 'react';
import { CheckCircle, Clock, MapPin, Ambulance } from 'lucide-react';

export default function StatusCard({ status, hospitalName, distance }) {
  
  const calculateETA = (dist) => {
    if (!dist) return "Calculating...";
    if (dist < 1) return "2-3 Mins";
    const minutes = Math.ceil(dist * 3) + 2;
    return `${minutes}-${minutes + 2} Mins`;
  };

  return (
    <div className="bg-white/95 backdrop-blur-xl rounded-3xl shadow-2xl shadow-slate-300/50 p-6 w-full max-w-md border border-white/50 animate-slide-up ring-1 ring-black/5">
      
      {/* Header */}
      <div className="flex items-center gap-4 mb-6 pb-6 border-b border-slate-100">
        <div className="bg-green-100 p-3 rounded-full shadow-inner">
           <CheckCircle className="text-green-600" size={28} strokeWidth={3} />
        </div>
        <div>
          <h3 className="text-xl font-bold text-slate-800 leading-tight">Help is on the way!</h3>
          <p className="text-sm text-slate-500 font-medium">Ambulance Dispatched</p>
        </div>
      </div>

      {/* Details Grid */}
      <div className="space-y-4">
        
        {/* Hospital Info */}
        <div className="bg-slate-50 p-4 rounded-2xl border border-slate-100 flex items-center gap-4">
          <div className="bg-white p-2 rounded-xl shadow-sm text-blue-600">
            <Ambulance size={24} />
          </div>
          <div>
            <p className="text-xs text-slate-400 uppercase font-bold tracking-wider mb-0.5">Assigned Unit</p>
            <p className="text-lg font-bold text-slate-900 leading-none">
              {hospitalName || "Searching..."}
            </p>
          </div>
        </div>
        
        {/* Stats Row */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-slate-50 p-3 rounded-2xl border border-slate-100 text-center">
             <div className="flex justify-center mb-1 text-orange-500"><Clock size={20} /></div>
             <p className="text-xs text-slate-400 font-bold uppercase">ETA</p>
             <p className="text-sm font-black text-slate-800">{calculateETA(distance)}</p>
          </div>

          <div className="bg-slate-50 p-3 rounded-2xl border border-slate-100 text-center">
             <div className="flex justify-center mb-1 text-blue-500"><MapPin size={20} /></div>
             <p className="text-xs text-slate-400 font-bold uppercase">Distance</p>
             <p className="text-sm font-black text-slate-800">{distance ? `${distance} km` : '--'}</p>
          </div>
        </div>

      </div>
      
      {/* Footer Strip */}
      <div className="mt-6 text-center">
        <p className="text-xs text-slate-400 font-medium">Do not close this app until help arrives.</p>
      </div>
    </div>
  );
}