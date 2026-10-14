import React from 'react';
import { Sparkles } from 'lucide-react';

interface WordCompleteBannerProps {
  word: string;
  points: number;
}

export const WordCompleteBanner: React.FC<WordCompleteBannerProps> = ({ word, points }) => {
  return (
    <div className="fixed top-18 left-1/2 -translate-x-1/2 z-50 pointer-events-none animate-pop-in">
      <div className="bg-gradient-to-r from-amber-400 via-yellow-300 to-amber-500 text-slate-900 px-5 py-2.5 rounded-full shadow-xl border-2 border-white flex items-center gap-2">
        <Sparkles className="w-5 h-5 text-amber-800 fill-amber-700 animate-spin" style={{ animationDuration: '3s' }} />
        <div className="flex flex-col items-center">
          <span className="text-[10px] font-black uppercase tracking-wider text-amber-900">
            Palavra Completa!
          </span>
          <span className="text-base sm:text-lg font-black tracking-tight text-slate-900">
            {word} <span className="text-emerald-700 font-extrabold">(+{points} pts!)</span>
          </span>
        </div>
        <Sparkles className="w-5 h-5 text-amber-800 fill-amber-700 animate-spin" style={{ animationDuration: '3s' }} />
      </div>
    </div>
  );
};
