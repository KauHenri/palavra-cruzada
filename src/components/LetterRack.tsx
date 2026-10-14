import React from 'react';
import type { Player, PendingPlacement } from '../types/game';
import { Check } from 'lucide-react';

interface LetterRackProps {
  player: Player;
  selectedHandIndex: number | null;
  unconfirmedPlacements: PendingPlacement[];
  onSelectTile: (index: number) => void;
  onConfirm: () => void;
}

export const LetterRack: React.FC<LetterRackProps> = ({
  player,
  selectedHandIndex,
  unconfirmedPlacements,
  onSelectTile,
  onConfirm
}) => {
  const placedIndices = new Set(unconfirmedPlacements.map(p => p.handIndex));
  const hasPlacements = unconfirmedPlacements.length > 0;

  return (
    <div className="w-full max-w-md mx-auto px-4 py-2 flex flex-col items-center gap-3">
      {/* Turn badge */}
      <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/70 backdrop-blur shadow-xs border border-slate-200">
        <span className="text-xs font-bold text-slate-500">Mão de</span>
        <span
          className="text-xs font-black truncate max-w-[120px]"
          style={{ color: player.color }}
        >
          {player.name}
        </span>
        <span className="text-xs">({player.hand.length} letras)</span>
      </div>

      {/* 5 Letter Tiles Rack */}
      <div className="flex items-center justify-center gap-2 sm:gap-3 w-full">
        {Array.from({ length: 5 }).map((_, idx) => {
          const letter = player.hand[idx];
          const isPlaced = placedIndices.has(idx);
          const isSelected = selectedHandIndex === idx;

          if (!letter) {
            // Empty rack slot (if hand has fewer than 5)
            return (
              <div
                key={`empty-slot-${idx}`}
                className="w-13 h-14 sm:w-15 sm:h-16 rounded-xl border-2 border-dashed border-slate-300/80 bg-slate-200/30 flex items-center justify-center"
              />
            );
          }

          if (isPlaced) {
            // Letter was placed on the board this turn
            return (
              <div
                key={`placed-slot-${idx}`}
                className="w-13 h-14 sm:w-15 sm:h-16 rounded-xl border-2 border-dashed border-amber-300 bg-amber-50/50 flex items-center justify-center text-amber-300 font-bold text-xs"
              >
                No grid
              </div>
            );
          }

          return (
            <button
              key={`tile-${idx}-${letter}`}
              onClick={() => onSelectTile(idx)}
              className={`w-13 h-14 sm:w-15 sm:h-16 rounded-xl font-black text-2xl sm:text-3xl flex items-center justify-center shadow-md transition-all cursor-pointer ${
                isSelected
                  ? 'bg-amber-100 text-slate-900 border-2 border-amber-500 -translate-y-2 shadow-amber-400/40 ring-4 ring-amber-300/50'
                  : 'bg-[#fffae8] text-slate-800 border-2 border-[#e6d8b8] hover:-translate-y-0.5 active:scale-95 shadow-slate-300/60'
              }`}
              style={{
                boxShadow: isSelected
                  ? '0 10px 15px -3px rgba(245, 158, 11, 0.3)'
                  : '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)'
              }}
            >
              {letter}
            </button>
          );
        })}
      </div>

      {/* Confirm Button */}
      <div className="w-full flex justify-center pt-1">
        <button
          onClick={onConfirm}
          disabled={!hasPlacements}
          className={`w-full max-w-xs py-3 px-6 rounded-2xl font-black text-base sm:text-lg flex items-center justify-center gap-2 shadow-md transition-all active:scale-95 cursor-pointer ${
            hasPlacements
              ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-blue-500/30 hover:brightness-105 ring-2 ring-blue-300'
              : 'bg-slate-200 text-slate-400 border border-slate-300 cursor-not-allowed shadow-none'
          }`}
        >
          <Check className="w-5 h-5 stroke-[3]" />
          <span>
            {hasPlacements
              ? `Confirmar Jogada (${unconfirmedPlacements.length})`
              : 'Coloque as letras no tabuleiro'}
          </span>
        </button>
      </div>
    </div>
  );
};
