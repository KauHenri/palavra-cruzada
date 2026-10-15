import React, { useState } from 'react';
import { Volume2, VolumeX, RotateCcw, Home, X, Save, Clock } from 'lucide-react';
import { soundManager } from '../utils/audio';

interface SettingsModalProps {
  player1Name: string;
  player2Name: string;
  turnTimeLimit: number;
  onUpdateNames: (p1: string, p2: string) => void;
  onUpdateTurnTimeLimit: (limit: number) => void;
  onRestartLevel: () => void;
  onGoToMenu: () => void;
  onClose: () => void;
}

export const SettingsModal: React.FC<SettingsModalProps> = ({
  player1Name,
  player2Name,
  turnTimeLimit,
  onUpdateNames,
  onUpdateTurnTimeLimit,
  onRestartLevel,
  onGoToMenu,
  onClose
}) => {
  const [p1, setP1] = useState(player1Name);
  const [p2, setP2] = useState(player2Name);
  const [timer, setTimer] = useState(turnTimeLimit);
  const [isMuted, setIsMuted] = useState(soundManager.getIsMuted());

  const handleToggleSound = () => {
    const muted = soundManager.toggleMute();
    setIsMuted(muted);
    if (!muted) {
      soundManager.playTileSelect();
    }
  };

  const handleSaveNames = (e: React.FormEvent) => {
    e.preventDefault();
    onUpdateNames(p1, p2);
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl max-w-sm w-full p-6 shadow-2xl border-2 border-slate-100 flex flex-col gap-4 animate-pop-in">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <h2 className="text-xl font-black text-slate-800">Configurações</h2>
          <button
            onClick={onClose}
            className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 hover:text-slate-800 cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Edit Names Form */}
        <form onSubmit={handleSaveNames} className="flex flex-col gap-3">
          <div className="flex flex-col gap-1">
            <label className="text-xs font-black text-slate-600 flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-blue-500" />
              Nome do Jogador 1:
            </label>
            <input
              type="text"
              value={p1}
              maxLength={15}
              onChange={e => setP1(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-300 text-slate-800 font-bold focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm"
              placeholder="Ex: Kauã"
            />
          </div>

          <div className="flex flex-col gap-1">
            <label className="text-xs font-black text-slate-600 flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-pink-500" />
              Nome do Jogador 2:
            </label>
            <input
              type="text"
              value={p2}
              maxLength={15}
              onChange={e => setP2(e.target.value)}
              className="w-full px-3 py-2 rounded-xl bg-slate-50 border border-slate-300 text-slate-800 font-bold focus:outline-none focus:ring-2 focus:ring-pink-500 text-sm"
              placeholder="Ex: Amor"
            />
          </div>

          <button
            type="submit"
            className="mt-1 w-full py-2 rounded-xl bg-blue-500 hover:bg-blue-600 text-white font-extrabold text-sm flex items-center justify-center gap-1.5 active:scale-95 transition-transform cursor-pointer"
          >
            <Save className="w-4 h-4" />
            <span>Salvar Nomes</span>
          </button>
        </form>

        <div className="h-px bg-slate-100 my-0.5" />

        {/* Turn Timer Selector */}
        <div className="flex flex-col gap-1.5 px-1">
          <div className="flex items-center justify-between">
            <span className="text-xs font-extrabold text-slate-700 flex items-center gap-1.5">
              <Clock className="w-3.5 h-3.5 text-sky-600" />
              Tempo por Turno:
            </span>
            <span className="text-xs font-black text-sky-600">
              {timer === 0 ? 'Sem limite' : `${timer}s`}
            </span>
          </div>

          <div className="grid grid-cols-4 gap-1.5 mt-0.5">
            {[
              { label: '60s', value: 60, desc: 'Rápido' },
              { label: '90s ⭐', value: 90, desc: 'Ideal' },
              { label: '120s', value: 120, desc: 'Tranquilo' },
              { label: '∞', value: 0, desc: 'Livre' }
            ].map(opt => (
              <button
                key={opt.value}
                type="button"
                onClick={() => {
                  setTimer(opt.value);
                  onUpdateTurnTimeLimit(opt.value);
                }}
                className={`py-1.5 px-1 rounded-xl font-black text-xs flex flex-col items-center justify-center transition-all cursor-pointer ${
                  timer === opt.value
                    ? 'bg-blue-500 text-white shadow-md shadow-blue-500/20 scale-102 ring-2 ring-blue-300'
                    : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                }`}
              >
                <span>{opt.label}</span>
                <span className={`text-[8px] font-bold ${timer === opt.value ? 'text-blue-100' : 'text-slate-400'}`}>
                  {opt.desc}
                </span>
              </button>
            ))}
          </div>
          <p className="text-[10px] font-bold text-slate-400 text-center">
            ⭐ 90s é o recomendado para um jogo dinâmico.
          </p>
        </div>

        <div className="h-px bg-slate-100 my-0.5" />

        {/* Audio Toggle */}
        <div className="flex items-center justify-between px-1">
          <span className="text-xs font-extrabold text-slate-700">Efeitos Sonoros</span>
          <button
            onClick={handleToggleSound}
            className={`px-3 py-1.5 rounded-xl font-black text-xs flex items-center gap-2 cursor-pointer transition-colors ${
              isMuted
                ? 'bg-rose-100 text-rose-700 border border-rose-200'
                : 'bg-emerald-100 text-emerald-700 border border-emerald-200'
            }`}
          >
            {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
            <span>{isMuted ? 'Mudo' : 'Ativado'}</span>
          </button>
        </div>

        {/* Level Controls */}
        <div className="flex flex-col gap-2 pt-2">
          <button
            onClick={() => {
              onRestartLevel();
              onClose();
            }}
            className="w-full py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-extrabold text-sm flex items-center justify-center gap-2 active:scale-95 transition-transform cursor-pointer"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Reiniciar Esta Fase</span>
          </button>

          <button
            onClick={() => {
              onGoToMenu();
              onClose();
            }}
            className="w-full py-2.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-extrabold text-sm flex items-center justify-center gap-2 active:scale-95 transition-transform cursor-pointer"
          >
            <Home className="w-4 h-4" />
            <span>Menu Principal / Seleção</span>
          </button>
        </div>
      </div>
    </div>
  );
};
