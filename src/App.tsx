import { useState, useEffect, useRef } from 'react';
import { LEVELS } from './data/levels';
import { useCrosswordGame } from './hooks/useCrosswordGame';
import { Header } from './components/Header';
import { ScoreBoard } from './components/ScoreBoard';
import { CrosswordGrid } from './components/CrosswordGrid';
import { LetterRack } from './components/LetterRack';
import { WordCompleteBanner } from './components/WordCompleteBanner';
import { TurnTimeoutBanner } from './components/TurnTimeoutBanner';
import { GameOverModal } from './components/GameOverModal';
import { SettingsModal } from './components/SettingsModal';
import { LevelSelect } from './components/LevelSelect';
import { MenuScreen } from './components/MenuScreen';

type ViewMode = 'menu' | 'level_select' | 'game';

export function App() {
  const [view, setView] = useState<ViewMode>('menu');
  const [currentLevelId, setCurrentLevelId] = useState<number>(1);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [exitToast, setExitToast] = useState(false);

  // References to keep event listeners always synced with current state
  const viewRef = useRef<ViewMode>(view);
  const isSettingsOpenRef = useRef<boolean>(isSettingsOpen);
  const lastBackPressRef = useRef<number>(0);

  useEffect(() => {
    viewRef.current = view;
  }, [view]);

  useEffect(() => {
    isSettingsOpenRef.current = isSettingsOpen;
  }, [isSettingsOpen]);

  // Set up history navigation stack to prevent Android back button from closing the app
  useEffect(() => {
    // Replace initial state with root, then push menu so there's always history behind it
    window.history.replaceState({ appView: 'root' }, '');
    window.history.pushState({ appView: 'menu' }, '');

    const onPopState = (e: PopStateEvent) => {
      // 1. If Settings Modal is open, back button simply closes the modal
      if (isSettingsOpenRef.current) {
        setIsSettingsOpen(false);
        return;
      }

      const state = e.state;

      // 2. If back reaches root (pressed back on menu)
      if (!state || state.appView === 'root') {
        const now = Date.now();
        if (now - lastBackPressRef.current < 2000) {
          // Double tap back within 2s -> let Android close/exit the app
          return;
        } else {
          lastBackPressRef.current = now;
          // Keep user in menu and show toast
          window.history.pushState({ appView: 'menu' }, '');
          setView('menu');
          setExitToast(true);
          setTimeout(() => setExitToast(false), 2000);
          return;
        }
      }

      // 3. Normal screen back navigation
      if (state.appView === 'menu' || state.appView === 'level_select' || state.appView === 'game') {
        setView(state.appView);
      } else {
        setView('menu');
      }
    };

    window.addEventListener('popstate', onPopState);
    return () => window.removeEventListener('popstate', onPopState);
  }, []);

  // Safe navigation helper that pushes state to history
  const navigateTo = (nextView: ViewMode) => {
    window.history.pushState({ appView: nextView }, '');
    setView(nextView);
  };

  const handleOpenSettings = () => {
    window.history.pushState({ appView: view, modal: 'settings' }, '');
    setIsSettingsOpen(true);
  };

  const handleCloseSettings = () => {
    if (isSettingsOpen) {
      setIsSettingsOpen(false);
      if (window.history.state?.modal === 'settings') {
        window.history.back();
      }
    }
  };

  // Stored player names
  const [p1Name, setP1Name] = useState(() => {
    return localStorage.getItem('pc_player1_name') || 'Kauã';
  });
  const [p2Name, setP2Name] = useState(() => {
    return localStorage.getItem('pc_player2_name') || 'Amor';
  });

  const currentLevel = LEVELS.find(l => l.id === currentLevelId) || LEVELS[0];

  const {
    players,
    currentTurn,
    grid,
    selectedHandIndex,
    selectedCell,
    unconfirmedPlacements,
    floatScores,
    wordCompleteBanner,
    turnTimeoutBanner,
    isGameOver,
    shakeCells,
    turnTimeLimit,
    timeLeft,
    handleSelectHandTile,
    handleCellClick,
    confirmTurn,
    initGame,
    updatePlayerNames,
    updateTurnTimeLimit
  } = useCrosswordGame({
    level: currentLevel,
    initialPlayer1Name: p1Name,
    initialPlayer2Name: p2Name,
    isPaused: isSettingsOpen || view !== 'game'
  });

  // Save names to local storage
  const handleUpdateNames = (newP1: string, newP2: string) => {
    setP1Name(newP1);
    setP2Name(newP2);
    localStorage.setItem('pc_player1_name', newP1);
    localStorage.setItem('pc_player2_name', newP2);
    updatePlayerNames(newP1, newP2);
  };

  const handleStartFromMenu = (newP1: string, newP2: string) => {
    handleUpdateNames(newP1, newP2);
    navigateTo('game');
  };

  const handleSelectLevel = (levelId: number) => {
    setCurrentLevelId(levelId);
    navigateTo('game');
  };

  const handleNextLevel = () => {
    const nextId = currentLevelId + 1;
    if (nextId <= LEVELS.length) {
      setCurrentLevelId(nextId);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#c8dcf0] via-[#dbeafe] to-[#e8f1fb] text-slate-800 flex flex-col justify-between relative overflow-hidden select-none">
      {/* Subtle Paris / Skyline background silhouette illustration */}
      <div className="absolute inset-0 pointer-events-none opacity-20 flex items-end justify-center overflow-hidden">
        <svg
          viewBox="0 0 1000 300"
          className="w-full max-w-2xl h-auto text-sky-900 fill-current opacity-25"
          preserveAspectRatio="none"
        >
          {/* Subtle Eiffel tower & rooftops silhouette */}
          <path d="M0,300 L0,240 Q100,220 200,240 L240,240 L245,210 L250,240 L380,240 L395,190 L400,240 L480,240 L490,130 L496,60 L500,20 L504,60 L510,130 L520,240 L620,240 L630,200 L640,240 L760,240 Q850,220 1000,240 L1000,300 Z" />
        </svg>
      </div>

      {/* Main View Router */}
      <div className="relative z-10 flex-1 flex flex-col w-full">
        {view === 'menu' && (
          <MenuScreen
            player1Name={p1Name}
            player2Name={p2Name}
            onStartGame={handleStartFromMenu}
            onOpenLevelSelect={() => navigateTo('level_select')}
            onOpenSettings={handleOpenSettings}
          />
        )}

        {view === 'level_select' && (
          <LevelSelect
            levels={LEVELS}
            currentLevelId={currentLevelId}
            onSelectLevel={handleSelectLevel}
            onBackToMenu={() => window.history.back()}
          />
        )}

        {view === 'game' && (
          <main className="w-full flex-1 flex flex-col justify-between py-1 max-w-md mx-auto">
            {/* Top Navigation */}
            <Header
              title={`${currentLevel.title}: ${currentLevel.subtitle}`}
              onBack={() => window.history.back()}
              onOpenSettings={handleOpenSettings}
            />

            {/* Scoreboard with Turn Timer */}
            <ScoreBoard
              players={players}
              currentTurn={currentTurn}
              timeLeft={timeLeft}
              turnTimeLimit={turnTimeLimit}
            />

            {/* The Swedish Crossword Grid */}
            <CrosswordGrid
              grid={grid}
              rows={currentLevel.rows}
              cols={currentLevel.cols}
              selectedCell={selectedCell}
              shakeCells={shakeCells}
              floatScores={floatScores}
              onCellClick={handleCellClick}
            />

            {/* 5-Letter Rack and Confirm Button */}
            <LetterRack
              player={players[currentTurn]}
              selectedHandIndex={selectedHandIndex}
              unconfirmedPlacements={unconfirmedPlacements}
              onSelectTile={handleSelectHandTile}
              onConfirm={confirmTurn}
            />

            {/* Word completion celebration toast */}
            {wordCompleteBanner && (
              <WordCompleteBanner
                word={wordCompleteBanner.word}
                points={wordCompleteBanner.points}
              />
            )}

            {/* Turn timeout toast */}
            {turnTimeoutBanner && (
              <TurnTimeoutBanner playerName={turnTimeoutBanner.playerName} />
            )}

            {/* Game Over Modal */}
            {isGameOver && (
              <GameOverModal
                players={players}
                hasNextLevel={currentLevelId < LEVELS.length}
                onNextLevel={handleNextLevel}
                onRestart={initGame}
                onGoToMenu={() => navigateTo('level_select')}
              />
            )}

            {/* Settings Modal */}
            {isSettingsOpen && (
              <SettingsModal
                player1Name={p1Name}
                player2Name={p2Name}
                turnTimeLimit={turnTimeLimit}
                onUpdateNames={handleUpdateNames}
                onUpdateTurnTimeLimit={updateTurnTimeLimit}
                onRestartLevel={initGame}
                onGoToMenu={() => {
                  setIsSettingsOpen(false);
                  navigateTo('menu');
                }}
                onClose={handleCloseSettings}
              />
            )}
          </main>
        )}
      </div>

      {/* Android double-back-to-exit Toast Notification */}
      {exitToast && (
        <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50 bg-slate-900/90 text-white px-4 py-2 rounded-full text-xs font-bold shadow-xl animate-pop-in pointer-events-none border border-slate-700">
          Toque em voltar novamente para sair
        </div>
      )}
    </div>
  );
}

export default App;
