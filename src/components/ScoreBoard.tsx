import React from 'react';
import type { Player, PlayerId } from '../types/game';
import { Clock } from 'lucide-react';

interface ScoreBoardProps {
  players: Record<PlayerId, Player>;
  currentTurn: PlayerId;
  timeLeft?: number;
  turnTimeLimit?: number;
}

export const ScoreBoard: React.FC<ScoreBoardProps> = ({
  players,
  currentTurn,
  timeLeft,
  turnTimeLimit = 0
}) => {
  const p1 = players.p1;
  const p2 = players.p2;

  const isP1Turn = currentTurn === 'p1';
  const isP2Turn = currentTurn === 'p2';

  const hasTimer = turnTimeLimit > 0 && timeLeft !== undefined;
  const minutes = hasTimer ? Math.floor(timeLeft / 60) : 0;
  const seconds = hasTimer ? timeLeft % 60 : 0;
  const timeFormatted = `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

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

        {/* Center Timer / Divider */}
        {hasTimer ? (
          <div
            className={`flex items-center gap-1 px-2.5 py-1 rounded-full border shadow-xs transition-all duration-300 ${
              timeLeft <= 10
                ? 'bg-rose-50 border-rose-400 text-rose-600 animate-pulse ring-2 ring-rose-200'
                : timeLeft <= 20
                ? 'bg-amber-50 border-amber-300 text-amber-600'
                : 'bg-white/90 border-slate-200 text-slate-700'
            }`}
          >
            <Clock
              className={`w-3.5 h-3.5 stroke-[2.5] ${
                timeLeft <= 10 ? 'animate-spin' : ''
              }`}
              style={timeLeft <= 10 ? { animationDuration: '3s' } : undefined}
            />
            <span className="font-mono font-black text-xs tracking-tight">
              {timeFormatted}
            </span>
          </div>
        ) : (
          <div className="text-slate-400 font-bold text-sm px-1 select-none">
            -
          </div>
        )}

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

      {/* Turn Timer Progress Bar */}
      {hasTimer && (
        <div className="w-full h-1.5 bg-slate-200/80 rounded-full mt-1.5 overflow-hidden shadow-inner">
          <div
            className={`h-full rounded-full transition-all duration-1000 ease-linear ${
              timeLeft <= 10
                ? 'bg-rose-500 animate-pulse'
                : timeLeft <= 20
                ? 'bg-amber-500'
                : isP1Turn
                ? 'bg-blue-500'
                : 'bg-pink-500'
            }`}
            style={{
              width: `${Math.min(100, Math.max(0, (timeLeft / turnTimeLimit) * 100))}%`
            }}
          />
        </div>
      )}
    </div>
  );
};
