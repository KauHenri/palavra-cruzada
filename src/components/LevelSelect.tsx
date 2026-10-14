import React from 'react';
import type { LevelDefinition } from '../types/game';
import { ChevronLeft, Play, Sparkles } from 'lucide-react';

interface LevelSelectProps {
  levels: LevelDefinition[];
  currentLevelId: number;
  onSelectLevel: (levelId: number) => void;
  onBackToMenu: () => void;
}

export const LevelSelect: React.FC<LevelSelectProps> = ({
  levels,
  currentLevelId,
  onSelectLevel,
  onBackToMenu
}) => {
  return (
    <div className="w-full max-w-md mx-auto min-h-screen px-4 py-4 flex flex-col">
      {/* Top Bar */}
      <div className="flex items-center justify-between mb-4">
        <button
          onClick={onBackToMenu}
          className="w-10 h-10 flex items-center justify-center rounded-full bg-white/80 backdrop-blur shadow-sm active:scale-95 transition-transform text-sky-600 border border-sky-100 cursor-pointer"
        >
          <ChevronLeft className="w-6 h-6 stroke-[2.5]" />
        </button>

        <h1 className="text-xl font-black text-slate-800 tracking-tight">
          Escolha uma Fase
        </h1>

        <div className="w-10 h-10" /> {/* Spacer */}
      </div>

      {/* Levels list */}
      <div className="flex-1 flex flex-col gap-3.5 overflow-y-auto pb-6">
        {levels.map((lvl) => {
          const isSelected = lvl.id === currentLevelId;

          return (
            <button
              key={lvl.id}
              onClick={() => onSelectLevel(lvl.id)}
              className={`w-full text-left p-4 rounded-3xl transition-all cursor-pointer relative overflow-hidden active:scale-98 ${
                isSelected
                  ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white shadow-lg shadow-blue-500/25 ring-2 ring-blue-300'
                  : 'bg-white/90 backdrop-blur text-slate-800 shadow-sm border border-sky-100 hover:shadow-md'
              }`}
            >
              {/* Badge for Level 4 */}
              {lvl.id === 4 && (
                <div className="absolute top-2 right-2 px-2.5 py-0.5 rounded-full bg-amber-400 text-slate-900 font-black text-[10px] flex items-center gap-1 shadow-sm">
                  <Sparkles className="w-3 h-3 fill-slate-900" />
                  <span>Grande Desafio (9x7)</span>
                </div>
              )}

              <div className="flex items-center justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span
                      className={`px-2.5 py-0.5 rounded-full text-xs font-black ${
                        isSelected
                          ? 'bg-white/20 text-white'
                          : 'bg-blue-50 text-blue-600'
                      }`}
                    >
                      Nível {lvl.id}
                    </span>
                    <span
                      className={`text-xs font-bold ${
                        isSelected ? 'text-blue-100' : 'text-slate-400'
                      }`}
                    >
                      {lvl.theme}
                    </span>
                  </div>

                  <h3 className="text-lg font-black tracking-tight leading-snug">
                    {lvl.subtitle}
                  </h3>

                  <div className="flex items-center gap-3 mt-2 text-xs font-semibold">
                    <span className={isSelected ? 'text-blue-100' : 'text-slate-500'}>
                      Grid {lvl.rows}x{lvl.cols}
                    </span>
                    <span className={isSelected ? 'text-blue-200' : 'text-slate-400'}>•</span>
                    <span className={isSelected ? 'text-blue-100' : 'text-slate-500'}>
                      {lvl.words.length} palavras
                    </span>
                  </div>
                </div>

                <div
                  className={`w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 transition-transform ${
                    isSelected
                      ? 'bg-white text-blue-600 shadow-md scale-105'
                      : 'bg-sky-50 text-sky-600'
                  }`}
                >
                  <Play className="w-6 h-6 fill-current ml-0.5" />
                </div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
