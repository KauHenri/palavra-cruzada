import React from 'react';
import { Clock } from 'lucide-react';

interface TurnTimeoutBannerProps {
  playerName: string;
}

export const TurnTimeoutBanner: React.FC<TurnTimeoutBannerProps> = ({ playerName }) => {
  return (
    <div className="fixed top-18 left-1/2 -translate-x-1/2 z-50 pointer-events-none animate-pop-in">
      <div className="bg-gradient-to-r from-rose-500 via-red-500 to-rose-600 text-white px-5 py-2.5 rounded-full shadow-2xl border-2 border-white/80 flex items-center gap-2.5">
        <Clock className="w-5 h-5 text-rose-100 animate-bounce" />
        <div className="flex flex-col items-center">
          <span className="text-[10px] font-black uppercase tracking-wider text-rose-100">
            Tempo Esgotado!
          </span>
          <span className="text-xs sm:text-sm font-extrabold text-white">
            A vez de <span className="underline decoration-white/50">{playerName}</span> acabou
          </span>
        </div>
      </div>
    </div>
  );
};
