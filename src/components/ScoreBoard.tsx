import React from 'react';
import type { Player, PlayerId } from '../types/game';

interface ScoreBoardProps {
  players: Record<PlayerId, Player>;
  currentTurn: PlayerId;
}

export const ScoreBoard: React.FC<ScoreBoardProps> = ({ players, currentTurn }) => {
  const p1 = players.p1;
  const p2 = players.p2;

  const isP1Turn = currentTurn === 'p1';
  const isP2Turn = currentTurn === 'p2';

  return (
    <div className="w-full max-w-md mx-auto px-3 py-1">
      <div className="flex items-center justify-between gap-2">
        {/* Player 1 Card */}
        <div
          className={`flex-1 flex items-center justify-end gap-2 px-2.5 py-1.5 rounded-2xl transition-all duration-300 ${
            isP1Turn
              ? 'bg-blue-500/15 border-2 border-blue-400 shadow-sm scale-102'
              : 'bg-white/60 border border-slate-200/80 opacity-75'
          }`}
        >
          <div className="flex flex-col items-end min-w-0">
            <span className="text-xs font-black truncate max-w-[90px] text-slate-800">
              {p1.name}
            </span>
            {isP1Turn && (
              <span className="text-[10px] font-bold text-blue-600 animate-pulse leading-none">
                Sua vez!
              </span>
            )}
          </div>

          <div
            className={`w-11 h-9 rounded-xl flex items-center justify-center font-black text-lg shadow-inner ${
              isP1Turn
                ? 'bg-blue-500 text-white shadow-blue-600/30 ring-2 ring-blue-300'
                : 'bg-slate-100 text-slate-600'
            }`}
          >
            {p1.score}
          </div>
        </div>

        {/* Divider */}
        <div className="text-slate-400 font-bold text-sm px-0.5 select-none">
          -
        </div>

        {/* Player 2 Card */}
        <div
          className={`flex-1 flex items-center justify-start gap-2 px-2.5 py-1.5 rounded-2xl transition-all duration-300 ${
            isP2Turn
              ? 'bg-pink-500/15 border-2 border-pink-400 shadow-sm scale-102'
              : 'bg-white/60 border border-slate-200/80 opacity-75'
          }`}
        >
          <div
            className={`w-11 h-9 rounded-xl flex items-center justify-center font-black text-lg shadow-inner ${
              isP2Turn
                ? 'bg-pink-500 text-white shadow-pink-600/30 ring-2 ring-pink-300'
                : 'bg-slate-100 text-slate-600'
            }`}
          >
            {p2.score}
          </div>

          <div className="flex flex-col items-start min-w-0">
            <span className="text-xs font-black truncate max-w-[90px] text-slate-800">
              {p2.name}
            </span>
            {isP2Turn && (
              <span className="text-[10px] font-bold text-pink-600 animate-pulse leading-none">
                Sua vez!
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
