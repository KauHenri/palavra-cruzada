import React from 'react';
import type { Player } from '../types/game';
import { Trophy, RotateCcw, ArrowRight, Home } from 'lucide-react';

interface GameOverModalProps {
  players: { p1: Player; p2: Player };
  hasNextLevel: boolean;
  onNextLevel: () => void;
  onRestart: () => void;
  onGoToMenu: () => void;
}

export const GameOverModal: React.FC<GameOverModalProps> = ({
  players,
  hasNextLevel,
  onNextLevel,
  onRestart,
  onGoToMenu
}) => {
  const p1 = players.p1;
  const p2 = players.p2;

  const isTie = p1.score === p2.score;
  const winner = p1.score > p2.score ? p1 : p2;

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl max-w-sm w-full p-6 shadow-2xl border-2 border-sky-100 flex flex-col items-center text-center animate-pop-in">
        {/* Trophy icon */}
        <div className="w-18 h-18 rounded-full bg-amber-100 text-amber-500 border-4 border-amber-300 flex items-center justify-center mb-3 shadow-lg">
          <Trophy className="w-10 h-10 fill-amber-400 stroke-[2]" />
        </div>

        <h2 className="text-2xl font-black text-slate-800 tracking-tight">
          {isTie ? 'Empate Emocionante!' : 'Temos um Vencedor!'}
        </h2>

        {!isTie && (
          <div className="mt-1 flex items-center gap-1.5 px-4 py-1 rounded-full bg-amber-50 border border-amber-200">
            <span className="text-xl">{winner.avatar}</span>
            <span className="text-base font-black text-amber-800">
              {winner.name} venceu a partida!
            </span>
          </div>
        )}

        {/* Final Score Cards */}
        <div className="w-full grid grid-cols-2 gap-3 my-5">
          {/* P1 */}
          <div
            className={`p-3 rounded-2xl border-2 flex flex-col items-center ${
              !isTie && winner.id === 'p1'
                ? 'bg-blue-50/70 border-blue-400 shadow-sm'
                : 'bg-slate-50 border-slate-200'
            }`}
          >
            <span className="text-xs font-black text-slate-600 truncate max-w-full">
              {p1.name}
            </span>
            <span className="text-3xl font-black text-blue-600 my-1">
              {p1.score}
            </span>
            <span className="text-[11px] text-slate-400 font-bold">pontos</span>
          </div>

          {/* P2 */}
          <div
            className={`p-3 rounded-2xl border-2 flex flex-col items-center ${
              !isTie && winner.id === 'p2'
                ? 'bg-pink-50/70 border-pink-400 shadow-sm'
                : 'bg-slate-50 border-slate-200'
            }`}
          >
            <span className="text-xs font-black text-slate-600 truncate max-w-full">
              {p2.name}
            </span>
            <span className="text-3xl font-black text-pink-600 my-1">
              {p2.score}
            </span>
            <span className="text-[11px] text-slate-400 font-bold">pontos</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="w-full flex flex-col gap-2.5">
          {hasNextLevel && (
            <button
              onClick={onNextLevel}
              className="w-full py-3.5 px-4 rounded-2xl bg-gradient-to-r from-blue-500 to-indigo-600 text-white font-black text-base flex items-center justify-center gap-2 shadow-lg shadow-blue-500/25 active:scale-95 transition-transform cursor-pointer"
            >
              <span>Próxima Fase</span>
              <ArrowRight className="w-5 h-5 stroke-[2.5]" />
            </button>
          )}

          <div className="flex gap-2 w-full">
            <button
              onClick={onRestart}
              className="flex-1 py-3 px-3 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-extrabold text-sm flex items-center justify-center gap-1.5 active:scale-95 transition-transform border border-slate-200 cursor-pointer"
            >
              <RotateCcw className="w-4 h-4" />
              <span>Jogar de Novo</span>
            </button>

            <button
              onClick={onGoToMenu}
              className="flex-1 py-3 px-3 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-extrabold text-sm flex items-center justify-center gap-1.5 active:scale-95 transition-transform border border-slate-200 cursor-pointer"
            >
              <Home className="w-4 h-4" />
              <span>Menu / Fases</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
