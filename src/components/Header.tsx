import React from 'react';
import { ChevronLeft, Settings } from 'lucide-react';

interface HeaderProps {
  title: string;
  onBack: () => void;
  onOpenSettings: () => void;
}

export const Header: React.FC<HeaderProps> = ({ title, onBack, onOpenSettings }) => {
  return (
    <header className="w-full flex items-center justify-between px-3 py-2.5 max-w-md mx-auto">
      {/* Back button */}
      <button
        onClick={onBack}
        className="w-10 h-10 flex items-center justify-center rounded-full bg-white/80 backdrop-blur shadow-sm active:scale-95 transition-transform text-sky-600 border border-sky-100"
        aria-label="Voltar para o menu"
      >
        <ChevronLeft className="w-6 h-6 stroke-[2.5]" />
      </button>

      {/* Level Title Pill */}
      <div className="px-5 py-1.5 rounded-full bg-white/90 backdrop-blur shadow-sm border border-sky-100 flex items-center justify-center">
        <h1 className="text-base sm:text-lg font-extrabold text-slate-700 tracking-tight">
          {title}
        </h1>
      </div>

      {/* Settings button */}
      <button
        onClick={onOpenSettings}
        className="w-10 h-10 flex items-center justify-center rounded-full bg-white/80 backdrop-blur shadow-sm active:scale-95 transition-transform text-sky-600 border border-sky-100"
        aria-label="Configurações"
      >
        <Settings className="w-5 h-5 stroke-[2.2]" />
      </button>
    </header>
  );
};
