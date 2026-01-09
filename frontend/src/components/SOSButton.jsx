import React from 'react';
import { AlertCircle, Loader2 } from 'lucide-react';

export default function SOSButton({ onClick, isLoading }) {
  return (
    <div className="flex flex-col items-center justify-center">
      {/* The Glow Effect Container */}
      <div className="relative group">
        
        {/* Pulsing Rings */}
        {!isLoading && (
          <>
            <div className="absolute top-0 left-0 w-full h-full bg-red-500 rounded-full opacity-20 animate-ping"></div>
            <div className="absolute -inset-4 bg-red-500 rounded-full opacity-10 animate-pulse delay-75"></div>
          </>
        )}

        {/* Main Button */}
        <button 
          onClick={onClick}
          disabled={isLoading}
          className={`
            relative z-10 w-48 h-48 md:w-56 md:h-56 rounded-full flex flex-col items-center justify-center
            transition-all duration-300 transform shadow-2xl shadow-red-600/40
            ${isLoading 
              ? 'bg-slate-800 cursor-not-allowed scale-95' 
              : 'bg-gradient-to-b from-red-500 to-red-700 hover:scale-105 hover:shadow-red-600/60 active:scale-95 border-4 border-red-400/30'
            }
          `}
        >
          <span className="text-white font-black tracking-widest flex flex-col items-center drop-shadow-md">
            {isLoading ? (
              <>
                <Loader2 size={56} className="animate-spin mb-3 opacity-80" />
                <span className="text-sm font-bold tracking-widest opacity-80">CONNECTING</span>
              </>
            ) : (
              <>
                <AlertCircle size={64} className="mb-2" strokeWidth={1.5} />
                <span className="text-5xl md:text-6xl font-black">SOS</span>
                <span className="text-[10px] font-bold mt-1 opacity-80 uppercase tracking-[0.2em]">Emergency</span>
              </>
            )}
          </span>
        </button>
      </div>
      
      <p className="mt-8 text-slate-600 bg-white/60 backdrop-blur-sm px-4 py-2 rounded-full text-xs font-bold tracking-wide shadow-sm border border-white">
        PRESS AND HOLD FOR IMMEDIATE ASSISTANCE
      </p>
    </div>
  );
}