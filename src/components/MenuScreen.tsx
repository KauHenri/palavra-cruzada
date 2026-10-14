import React, { useState, useEffect } from 'react';
import { Play, Grid, Users, Info, Heart, Download } from 'lucide-react';

interface MenuScreenProps {
  player1Name: string;
  player2Name: string;
  onStartGame: (p1Name: string, p2Name: string) => void;
  onOpenLevelSelect: () => void;
}

export const MenuScreen: React.FC<MenuScreenProps> = ({
  player1Name,
  player2Name,
  onStartGame,
  onOpenLevelSelect
}) => {
  const [p1, setP1] = useState(player1Name);
  const [p2, setP2] = useState(player2Name);
  const [showRules, setShowRules] = useState(false);
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null);

  useEffect(() => {
    const handler = (e: any) => {
      e.preventDefault();
      setDeferredPrompt(e);
    };
    window.addEventListener('beforeinstallprompt', handler);
    return () => window.removeEventListener('beforeinstallprompt', handler);
  }, []);

  const handleInstallApp = async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const choice = await deferredPrompt.userChoice;
      if (choice.outcome === 'accepted') {
        setDeferredPrompt(null);
      }
    }
  };

  const handleStart = () => {
    onStartGame(p1 || 'Jogador 1', p2 || 'Jogador 2');
  };

  return (
    <div className="w-full max-w-md mx-auto min-h-screen px-4 py-6 flex flex-col justify-between items-center text-center">
      {/* Header / Hero */}
      <div className="w-full flex flex-col items-center pt-4">
        {/* Logo / Badge */}
        <div className="w-20 h-20 rounded-3xl bg-gradient-to-tr from-blue-500 to-indigo-600 text-white shadow-xl shadow-blue-500/30 flex items-center justify-center mb-3 border-2 border-white/60">
          <div className="grid grid-cols-2 gap-1 p-2">
            <span className="w-6 h-6 rounded-md bg-white text-blue-600 font-black text-sm flex items-center justify-center shadow-xs">
              P
            </span>
            <span className="w-6 h-6 rounded-md bg-amber-300 text-slate-800 font-black text-sm flex items-center justify-center shadow-xs">
              C
            </span>
            <span className="w-6 h-6 rounded-md bg-pink-400 text-white font-black text-sm flex items-center justify-center shadow-xs">
              ♥
            </span>
            <span className="w-6 h-6 rounded-md bg-white text-indigo-600 font-black text-sm flex items-center justify-center shadow-xs">
              X
            </span>
          </div>
        </div>

        <h1 className="text-3xl sm:text-4xl font-black text-slate-800 tracking-tight leading-tight">
          Palavras Cruzadas
        </h1>
        <p className="text-sm font-extrabold text-blue-600 tracking-wide mt-1 flex items-center justify-center gap-1">
          Duelo Competitivo Local <Heart className="w-3.5 h-3.5 fill-pink-500 text-pink-500" />
        </p>
      </div>

      {/* Players Setup Card */}
      <div className="w-full bg-white/90 backdrop-blur rounded-3xl p-5 shadow-sm border border-sky-100 flex flex-col gap-3.5 my-4">
        <div className="flex items-center gap-2 text-slate-700 font-black text-sm justify-center mb-1">
          <Users className="w-4 h-4 text-blue-600" />
          <span>Personalizar Jogadores</span>
        </div>

        {/* Player 1 input */}
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-xl bg-blue-100 text-blue-600 font-black text-sm flex items-center justify-center shrink-0">
            J1
          </div>
          <input
            type="text"
            value={p1}
            maxLength={15}
            onChange={e => setP1(e.target.value)}
            className="flex-1 px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 font-bold focus:outline-none focus:ring-2 focus:ring-blue-400 text-sm"
            placeholder="Nome do Jogador 1 (ex: Kauã)"
          />
        </div>

        {/* Player 2 input */}
        <div className="flex items-center gap-2">
          <div className="w-9 h-9 rounded-xl bg-pink-100 text-pink-600 font-black text-sm flex items-center justify-center shrink-0">
            J2
          </div>
          <input
            type="text"
            value={p2}
            maxLength={15}
            onChange={e => setP2(e.target.value)}
            className="flex-1 px-3.5 py-2.5 rounded-xl bg-slate-50 border border-slate-200 text-slate-800 font-bold focus:outline-none focus:ring-2 focus:ring-pink-400 text-sm"
            placeholder="Nome do Jogador 2 (ex: Amor)"
          />
        </div>
      </div>

      {/* Action Buttons */}
      <div className="w-full flex flex-col gap-3">
        <button
          onClick={handleStart}
          className="w-full py-4 px-6 rounded-2xl bg-gradient-to-r from-blue-500 via-indigo-600 to-blue-600 text-white font-black text-lg flex items-center justify-center gap-2 shadow-xl shadow-blue-500/30 active:scale-95 transition-transform cursor-pointer hover:brightness-105"
        >
          <Play className="w-6 h-6 fill-current" />
          <span>Jogar Agora</span>
        </button>

        <button
          onClick={onOpenLevelSelect}
          className="w-full py-3.5 px-6 rounded-2xl bg-white/90 hover:bg-white text-slate-700 font-extrabold text-base flex items-center justify-center gap-2 shadow-sm border border-slate-200 active:scale-95 transition-transform cursor-pointer"
        >
          <Grid className="w-5 h-5 text-indigo-600" />
          <span>Selecionar Fases</span>
        </button>

        {deferredPrompt && (
          <button
            onClick={handleInstallApp}
            className="w-full py-3.5 px-6 rounded-2xl bg-gradient-to-r from-emerald-500 to-teal-600 text-white font-black text-base flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/25 active:scale-95 transition-transform cursor-pointer hover:brightness-105 animate-pulse"
          >
            <Download className="w-5 h-5 stroke-[2.5]" />
            <span>📲 Instalar Aplicativo no Celular</span>
          </button>
        )}

        <button
          onClick={() => setShowRules(!showRules)}
          className="py-2 text-xs font-black text-slate-500 hover:text-blue-600 flex items-center justify-center gap-1 cursor-pointer transition-colors"
        >
          <Info className="w-3.5 h-3.5" />
          <span>{showRules ? 'Ocultar Regras' : 'Como Funciona a Pontuação?'}</span>
        </button>
      </div>

      {/* Rules Dropdown Box */}
      {showRules && (
        <div className="w-full bg-white/95 rounded-2xl p-4 mt-3 shadow-md border border-slate-200 text-left text-xs text-slate-700 flex flex-col gap-2 animate-pop-in">
          <h4 className="font-black text-slate-900 border-b pb-1 text-sm">
            📜 Regras Oficiais do Duelo:
          </h4>
          <p>
            • <strong>5 Letras por Turno:</strong> Cada jogador recebe 5 letras por vez para posicionar no tabuleiro.
          </p>
          <p>
            • <strong>Botão Confirmar:</strong> Posicione quantas letras quiser e toque em Confirmar.
          </p>
          <p>
            • <strong>Pontos por Letra:</strong> Cada letra certa vale <span className="text-emerald-600 font-bold">+1 ponto</span>. Letra errada desconta <span className="text-rose-600 font-bold">-1 ponto</span>.
          </p>
          <p>
            • <strong>Letras Erradas:</strong> Voltam direto para a sua mão para tentar na próxima rodada!
          </p>
          <p>
            • <strong>Bônus de Palavra:</strong> Ao fechar a última letra de qualquer palavra, você ganha pontos extras iguais ao tamanho da palavra!
          </p>
          <p>
            • <strong>Vencedor:</strong> Vence quem somar mais pontos ao completar o tabuleiro!
          </p>
        </div>
      )}

      {/* Footer */}
      <footer className="pt-4 text-[11px] font-bold text-slate-400">
        Feito para jogar a dois no celular • 100% Offline
      </footer>
    </div>
  );
};
