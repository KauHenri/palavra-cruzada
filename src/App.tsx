import { useState } from 'react';
import { LEVELS } from './data/levels';
import { useCrosswordGame } from './hooks/useCrosswordGame';
import { Header } from './components/Header';
import { ScoreBoard } from './components/ScoreBoard';
import { CrosswordGrid } from './components/CrosswordGrid';
import { LetterRack } from './components/LetterRack';
import { WordCompleteBanner } from './components/WordCompleteBanner';
import { GameOverModal } from './components/GameOverModal';
import { SettingsModal } from './components/SettingsModal';
import { LevelSelect } from './components/LevelSelect';
import { MenuScreen } from './components/MenuScreen';

type ViewMode = 'menu' | 'level_select' | 'game';

export function App() {
  const [view, setView] = useState<ViewMode>('menu');
  const [currentLevelId, setCurrentLevelId] = useState<number>(1);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

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
    isGameOver,
    shakeCells,
    handleSelectHandTile,
    handleCellClick,
    confirmTurn,
    initGame,
    updatePlayerNames
  } = useCrosswordGame({
    level: currentLevel,
    initialPlayer1Name: p1Name,
    initialPlayer2Name: p2Name
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
    setView('game');
  };

  const handleSelectLevel = (levelId: number) => {
    setCurrentLevelId(levelId);
    setView('game');
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
            onOpenLevelSelect={() => setView('level_select')}
          />
        )}

        {view === 'level_select' && (
          <LevelSelect
            levels={LEVELS}
            currentLevelId={currentLevelId}
            onSelectLevel={handleSelectLevel}
            onBackToMenu={() => setView('menu')}
          />
        )}

        {view === 'game' && (
          <main className="w-full flex-1 flex flex-col justify-between py-1 max-w-md mx-auto">
            {/* Top Navigation */}
            <Header
              title={`${currentLevel.title}: ${currentLevel.subtitle}`}
              onBack={() => setView('level_select')}
              onOpenSettings={() => setIsSettingsOpen(true)}
            />

            {/* Scoreboard */}
            <ScoreBoard players={players} currentTurn={currentTurn} />

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

            {/* Game Over Modal */}
            {isGameOver && (
              <GameOverModal
                players={players}
                hasNextLevel={currentLevelId < LEVELS.length}
                onNextLevel={handleNextLevel}
                onRestart={initGame}
                onGoToMenu={() => setView('level_select')}
              />
            )}

            {/* Settings Modal */}
            {isSettingsOpen && (
              <SettingsModal
                player1Name={p1Name}
                player2Name={p2Name}
                onUpdateNames={handleUpdateNames}
                onRestartLevel={initGame}
                onGoToMenu={() => setView('menu')}
                onClose={() => setIsSettingsOpen(false)}
              />
            )}
          </main>
        )}
      </div>
    </div>
  );
}

export default App;
