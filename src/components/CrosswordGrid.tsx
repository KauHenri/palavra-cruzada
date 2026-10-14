import React from 'react';
import type { GridCell, GridCellLetter, GridCellClue, FloatScoreNotification } from '../types/game';

interface CrosswordGridProps {
  grid: GridCell[][];
  rows: number;
  cols: number;
  selectedCell: { row: number; col: number } | null;
  shakeCells: { row: number; col: number }[];
  floatScores: FloatScoreNotification[];
  onCellClick: (row: number, col: number) => void;
}

export const CrosswordGrid: React.FC<CrosswordGridProps> = ({
  grid,
  rows,
  cols,
  selectedCell,
  shakeCells,
  floatScores,
  onCellClick
}) => {
  return (
    <div className="w-full max-w-md mx-auto px-2 py-1.5 flex items-center justify-center">
      <div
        className="w-full bg-white rounded-xl shadow-md border-2 border-slate-300 overflow-hidden relative select-none"
        style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))`,
          gridTemplateRows: `repeat(${rows}, minmax(0, 1fr))`,
          aspectRatio: `${cols} / ${rows}`
        }}
      >
        {grid.map((row, rIdx) =>
          row.map((cell, cIdx) => {
            const isSelected = selectedCell?.row === rIdx && selectedCell?.col === cIdx;
            const isShaking = shakeCells.some(s => s.row === rIdx && s.col === cIdx);

            if (cell.type === 'empty') {
              return (
                <div
                  key={`empty-${rIdx}-${cIdx}`}
                  className="bg-slate-200/50 border-[0.5px] border-slate-300/80"
                />
              );
            }

            if (cell.type === 'clue') {
              return (
                <ClueCellComponent
                  key={`clue-${rIdx}-${cIdx}`}
                  cell={cell}
                  rIdx={rIdx}
                  cIdx={cIdx}
                />
              );
            }

            return (
              <LetterCellComponent
                key={`letter-${rIdx}-${cIdx}`}
                cell={cell}
                rIdx={rIdx}
                cIdx={cIdx}
                isSelected={isSelected}
                isShaking={isShaking}
                onClick={() => onCellClick(rIdx, cIdx)}
              />
            );
          })
        )}

        {/* Floating Scores Overlay */}
        {floatScores.map(score => {
          const topPercent = (score.row / rows) * 100;
          const leftPercent = (score.col / cols) * 100;

          return (
            <div
              key={score.id}
              className={`absolute pointer-events-none z-30 font-black text-sm sm:text-base animate-float-score drop-shadow-md ${
                score.type === 'correct'
                  ? 'text-emerald-500 bg-white/90 px-1.5 py-0.5 rounded-full border border-emerald-300'
                  : score.type === 'wrong'
                  ? 'text-rose-500 bg-white/90 px-1.5 py-0.5 rounded-full border border-rose-300'
                  : 'text-amber-500 bg-white/95 px-2 py-0.5 rounded-full border-2 border-amber-400 text-xs sm:text-sm'
              }`}
              style={{
                top: `${topPercent}%`,
                left: `${leftPercent}%`,
                transform: 'translate(10%, -50%)'
              }}
            >
              {score.text}
            </div>
          );
        })}
      </div>
    </div>
  );
};

// Clue Cell renderer matching authentic Swedish Crossword ("Cruzadas Diretas") style
const ClueCellComponent: React.FC<{ cell: GridCellClue; rIdx: number; cIdx: number }> = ({ cell }) => {
  const clues = cell.clues;
  const isDual = clues.length > 1;

  // Responsive font size based on character count so text never clips
  const getFontSize = (text: string, isDualPart: boolean) => {
    const len = text.length;
    if (isDualPart) {
      if (len <= 5) return 'text-[7.5px] sm:text-[9px]';
      if (len <= 9) return 'text-[6.5px] sm:text-[8px]';
      return 'text-[5.5px] sm:text-[7px]';
    } else {
      if (len <= 6) return 'text-[8.5px] sm:text-[10px]';
      if (len <= 11) return 'text-[7px] sm:text-[8.5px]';
      return 'text-[6px] sm:text-[7.5px]';
    }
  };

  return (
    <div className="bg-[#e4effb] border-[0.5px] border-slate-300 p-0.5 overflow-hidden relative select-none w-full h-full flex flex-col justify-between">
      {isDual ? (
        // Dual clue cell: split top and bottom with clean divider
        <div className="h-full w-full flex flex-col divide-y divide-blue-300">
          {/* Top clue: typically points RIGHT */}
          <div className="flex-1 flex items-center justify-between px-0.5 py-0.5 min-h-0 gap-0.5">
            <span className={`${getFontSize(clues[0]?.text || '', true)} font-black tracking-tighter text-slate-900 leading-[1.0] break-words flex-1 text-center uppercase`}>
              {clues[0]?.text}
            </span>
            <div className="shrink-0 flex items-center justify-center pl-0.5">
              <svg className="w-2 h-2 text-blue-700 fill-current" viewBox="0 0 10 10">
                {clues[0]?.direction === 'right' ? (
                  <polygon points="1,1 9,5 1,9" />
                ) : (
                  <polygon points="1,1 9,1 5,9" />
                )}
              </svg>
            </div>
          </div>

          {/* Bottom clue: typically points DOWN */}
          <div className="flex-1 flex flex-col items-center justify-between px-0.5 pt-0.5 pb-0.5 min-h-0">
            <span className={`${getFontSize(clues[1]?.text || '', true)} font-black tracking-tighter text-slate-900 leading-[1.0] break-words text-center flex-1 flex items-center uppercase`}>
              {clues[1]?.text}
            </span>
            <div className="shrink-0 flex items-center justify-center">
              <svg className="w-2 h-2 text-blue-700 fill-current" viewBox="0 0 10 10">
                {clues[1]?.direction === 'right' ? (
                  <polygon points="1,1 9,5 1,9" />
                ) : (
                  <polygon points="1,1 9,1 5,9" />
                )}
              </svg>
            </div>
          </div>
        </div>
      ) : (
        // Single clue cell
        <div className="h-full w-full flex flex-col justify-between p-0.5">
          {clues[0]?.direction === 'right' ? (
            // Clue pointing RIGHT: text centered with full cell width, arrow at bottom-right
            <div className="h-full w-full flex flex-col justify-between">
              <div className="flex-1 flex items-center justify-center px-0.5 text-center">
                <span className={`${getFontSize(clues[0]?.text || '', false)} font-black tracking-tight text-slate-900 leading-[1.05] break-words uppercase`}>
                  {clues[0]?.text}
                </span>
              </div>
              <div className="flex justify-end items-center shrink-0 pr-0.5 pb-0.5">
                <svg className="w-2 h-2 text-blue-700 fill-current" viewBox="0 0 10 10">
                  <polygon points="1,1 9,5 1,9" />
                </svg>
              </div>
            </div>
          ) : (
            // Clue pointing DOWN: text centered, arrow at bottom center
            <div className="h-full w-full flex flex-col items-center justify-between">
              <div className="flex-1 flex items-center justify-center px-0.5 text-center">
                <span className={`${getFontSize(clues[0]?.text || '', false)} font-black tracking-tight text-slate-900 leading-[1.05] break-words uppercase`}>
                  {clues[0]?.text}
                </span>
              </div>
              <div className="shrink-0 flex items-center justify-center pb-0.5">
                <svg className="w-2 h-2 text-blue-700 fill-current" viewBox="0 0 10 10">
                  <polygon points="1,1 9,1 5,9" />
                </svg>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

// Letter Cell renderer
interface LetterCellProps {
  cell: GridCellLetter;
  rIdx: number;
  cIdx: number;
  isSelected: boolean;
  isShaking: boolean;
  onClick: () => void;
}

const LetterCellComponent: React.FC<LetterCellProps> = ({
  cell,
  isSelected,
  isShaking,
  onClick
}) => {
  const isLocked = cell.isLocked;
  const currentLetter = cell.currentLetter;
  const confirmedBy = cell.confirmedBy;

  let bgClass = 'bg-white';
  let borderClass = 'border-[0.5px] border-slate-300';
  let textClass = 'text-slate-800';

  if (isLocked) {
    bgClass = confirmedBy === 'p1' ? 'bg-blue-50/40' : 'bg-pink-50/40';
    textClass = 'text-slate-900 font-black';
  } else if (currentLetter) {
    // Unconfirmed placed letter
    bgClass = 'bg-amber-100/90';
    borderClass = 'border-2 border-amber-400 shadow-sm';
    textClass = 'text-amber-900 font-black';
  } else if (isSelected) {
    bgClass = 'bg-sky-100/80';
    borderClass = 'border-2 border-sky-500 ring-2 ring-sky-300';
  }

  return (
    <button
      onClick={onClick}
      disabled={isLocked}
      className={`relative w-full h-full flex items-center justify-center transition-all ${bgClass} ${borderClass} ${textClass} ${
        isShaking ? 'animate-shake bg-rose-100 border-rose-400 text-rose-600' : ''
      } ${!isLocked ? 'cursor-pointer active:scale-95' : 'cursor-default'}`}
    >
      {/* Confirmed / Locked Letter */}
      {isLocked && (
        <span className="text-base sm:text-xl font-black animate-pop-in">
          {cell.displayChar || cell.solution}
        </span>
      )}

      {/* Unconfirmed Letter Placed by Player */}
      {!isLocked && currentLetter && (
        <span className="text-base sm:text-xl font-black text-amber-900 animate-pop-in">
          {currentLetter}
        </span>
      )}

      {/* Player confirmation badge dot in corner */}
      {isLocked && confirmedBy && (
        <div
          className={`absolute bottom-0.5 right-0.5 w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full ${
            confirmedBy === 'p1' ? 'bg-blue-500' : 'bg-pink-500'
          }`}
        />
      )}
    </button>
  );
};
