import { useState, useEffect, useCallback } from 'react';
import type { Player, PlayerId, LevelDefinition, GridCell, GridCellLetter, PendingPlacement, FloatScoreNotification } from '../types/game';
import { soundManager } from '../utils/audio';
import confetti from 'canvas-confetti';

interface UseCrosswordGameProps {
  level: LevelDefinition;
  initialPlayer1Name?: string;
  initialPlayer2Name?: string;
  onGameOver?: (winner: Player | 'tie', p1: Player, p2: Player) => void;
}

export function useCrosswordGame({
  level,
  initialPlayer1Name = 'Jogador 1',
  initialPlayer2Name = 'Jogador 2',
  onGameOver
}: UseCrosswordGameProps) {
  // Players state
  const [players, setPlayers] = useState<Record<PlayerId, Player>>({
    p1: {
      id: 'p1',
      name: initialPlayer1Name,
      score: 0,
      hand: [],
      color: '#3b82f6', // Blue
      avatar: '👦'
    },
    p2: {
      id: 'p2',
      name: initialPlayer2Name,
      score: 0,
      hand: [],
      color: '#ec4899', // Pink
      avatar: '👧'
    }
  });

  const [currentTurn, setCurrentTurn] = useState<PlayerId>('p1');
  const [grid, setGrid] = useState<GridCell[][]>([]);
  const [remainingPool, setRemainingPool] = useState<string[]>([]);
  const [selectedHandIndex, setSelectedHandIndex] = useState<number | null>(null);
  const [selectedCell, setSelectedCell] = useState<{ row: number; col: number } | null>(null);
  const [unconfirmedPlacements, setUnconfirmedPlacements] = useState<PendingPlacement[]>([]);
  const [floatScores, setFloatScores] = useState<FloatScoreNotification[]>([]);
  const [wordCompleteBanner, setWordCompleteBanner] = useState<{ word: string; points: number } | null>(null);
  const [isGameOver, setIsGameOver] = useState(false);
  const [completedWordIds, setCompletedWordIds] = useState<Set<string>>(new Set());
  const [shakeCells, setShakeCells] = useState<{ row: number; col: number }[]>([]);

  // Initialize or reset game when level changes
  const initGame = useCallback(() => {
    // Clone grid from level and set starter letters (if any)
    const newGrid: GridCell[][] = level.grid.map((row, rIdx) =>
      row.map((cell, cIdx) => {
        if (cell.type === 'letter') {
          // In Level 1 (the screenshot puzzle), (1,1)=A, (2,5)=O, (5,2)=L, (5,6)=E start pre-revealed!
          const isStarter = level.id === 1 && (
            (rIdx === 1 && cIdx === 1) ||
            (rIdx === 2 && cIdx === 5) ||
            (rIdx === 5 && cIdx === 2) ||
            (rIdx === 5 && cIdx === 6)
          );

          return {
            ...cell,
            currentLetter: null,
            isLocked: isStarter,
            confirmedBy: null
          };
        }
        return { ...cell };
      })
    );

    // Extract undiscovered solution letters from the grid
    const allLetters: string[] = [];
    newGrid.forEach(row => {
      row.forEach(cell => {
        if (cell.type === 'letter' && !cell.isLocked) {
          allLetters.push(cell.solution);
        }
      });
    });

    // Shuffle pool
    const pool = [...allLetters].sort(() => Math.random() - 0.5);

    // Deal 5 letters to Player 1 and 5 letters to Player 2
    const p1Hand = pool.splice(0, Math.min(5, pool.length));
    const p2Hand = pool.splice(0, Math.min(5, pool.length));

    setPlayers(prev => ({
      p1: { ...prev.p1, score: 0, hand: p1Hand },
      p2: { ...prev.p2, score: 0, hand: p2Hand }
    }));

    setGrid(newGrid);
    setRemainingPool(pool);
    setCurrentTurn('p1');
    setSelectedHandIndex(null);
    setSelectedCell(null);
    setUnconfirmedPlacements([]);
    setFloatScores([]);
    setWordCompleteBanner(null);
    setIsGameOver(false);
    setCompletedWordIds(new Set());
    setShakeCells([]);
  }, [level]);

  useEffect(() => {
    initGame();
  }, [initGame]);

  // Select a tile from the current player's hand
  const handleSelectHandTile = (index: number) => {
    // If clicking already selected tile, unselect it
    if (selectedHandIndex === index) {
      setSelectedHandIndex(null);
      return;
    }

    soundManager.playTileSelect();
    setSelectedHandIndex(index);

    // If a valid letter cell was already selected on the grid, place it immediately!
    if (selectedCell) {
      placeLetterOnCell(selectedCell.row, selectedCell.col, index);
      setSelectedCell(null);
      setSelectedHandIndex(null);
    }
  };

  // Helper to place letter from hand to a cell
  const placeLetterOnCell = (row: number, col: number, handIdx: number) => {
    const targetCell = grid[row]?.[col];
    if (!targetCell || targetCell.type !== 'letter' || targetCell.isLocked) {
      return;
    }

    const currentHand = players[currentTurn].hand;
    const letterToPlace = currentHand[handIdx];
    if (!letterToPlace) return;

    // Check if this cell already has an unconfirmed placement
    const existingPlacement = unconfirmedPlacements.find(p => p.row === row && p.col === col);
    let updatedPlacements = [...unconfirmedPlacements];

    if (existingPlacement) {
      // Return previous letter to hand
      updatedPlacements = updatedPlacements.filter(p => !(p.row === row && p.col === col));
    }

    // Add new placement
    updatedPlacements.push({
      row,
      col,
      letter: letterToPlace,
      handIndex: handIdx
    });

    // Update grid state with currentLetter
    setGrid(prev =>
      prev.map((r, rIdx) =>
        r.map((c, cIdx) => {
          if (rIdx === row && cIdx === col && c.type === 'letter') {
            return { ...c, currentLetter: letterToPlace };
          }
          return c;
        })
      )
    );

    setUnconfirmedPlacements(updatedPlacements);
    soundManager.playTilePlace();
  };

  // Handle clicking a cell on the grid
  const handleCellClick = (row: number, col: number) => {
    const targetCell = grid[row]?.[col];
    if (!targetCell || targetCell.type !== 'letter' || targetCell.isLocked) {
      setSelectedCell(null);
      return;
    }

    // Check if cell has an unconfirmed placement from this turn
    const placementIndex = unconfirmedPlacements.findIndex(p => p.row === row && p.col === col);

    if (placementIndex !== -1) {
      // Tap on an unconfirmed placed letter -> Remove it and return to rack!
      const newPlacements = unconfirmedPlacements.filter((_, idx) => idx !== placementIndex);
      setUnconfirmedPlacements(newPlacements);

      setGrid(prev =>
        prev.map((r, rIdx) =>
          r.map((c, cIdx) => {
            if (rIdx === row && cIdx === col && c.type === 'letter') {
              return { ...c, currentLetter: null };
            }
            return c;
          })
        )
      );

      soundManager.playTileRemove();
      return;
    }

    // If user has a tile selected in hand, place it here!
    if (selectedHandIndex !== null) {
      placeLetterOnCell(row, col, selectedHandIndex);
      setSelectedHandIndex(null);
      setSelectedCell(null);
    } else {
      // Highlight this empty cell waiting for tile selection
      setSelectedCell(prev => (prev?.row === row && prev?.col === col ? null : { row, col }));
      soundManager.playTileSelect();
    }
  };

  // Trigger floating score notification
  const addFloatScore = (row: number, col: number, text: string, type: 'correct' | 'wrong' | 'bonus') => {
    const id = `${row}-${col}-${Date.now()}-${Math.random()}`;
    setFloatScores(prev => [...prev, { id, row, col, text, type }]);
    setTimeout(() => {
      setFloatScores(prev => prev.filter(f => f.id !== id));
    }, 1200);
  };

  // Confirm turn
  const confirmTurn = () => {
    if (unconfirmedPlacements.length === 0) {
      return;
    }

    let turnScoreChange = 0;
    const correctPlacements: PendingPlacement[] = [];
    const wrongPlacements: PendingPlacement[] = [];
    const shakes: { row: number; col: number }[] = [];

    // Evaluate each placement
    unconfirmedPlacements.forEach(placement => {
      const cell = grid[placement.row][placement.col] as GridCellLetter;
      if (placement.letter === cell.solution) {
        correctPlacements.push(placement);
        turnScoreChange += 1;
        addFloatScore(placement.row, placement.col, '+1', 'correct');
      } else {
        wrongPlacements.push(placement);
        turnScoreChange -= 1;
        shakes.push({ row: placement.row, col: placement.col });
        addFloatScore(placement.row, placement.col, '-1', 'wrong');
      }
    });

    if (shakes.length > 0) {
      setShakeCells(shakes);
      setTimeout(() => setShakeCells([]), 600);
      soundManager.playWrong();
    } else {
      soundManager.playCorrect();
    }

    // Update grid: correct letters get locked, wrong letters get cleared
    const nextGrid: GridCell[][] = grid.map((r, rIdx) =>
      r.map((c, cIdx) => {
        if (c.type !== 'letter') return c;

        const isCorrect = correctPlacements.some(p => p.row === rIdx && p.col === cIdx);
        if (isCorrect) {
          return {
            ...c,
            currentLetter: null,
            isLocked: true,
            confirmedBy: currentTurn
          };
        }

        const isWrong = wrongPlacements.some(p => p.row === rIdx && p.col === cIdx);
        if (isWrong) {
          return {
            ...c,
            currentLetter: null
          };
        }

        return c;
      })
    );

    // Check newly completed words
    const newlyCompletedWords: { word: string; points: number }[] = [];
    const updatedCompletedWordIds = new Set(completedWordIds);

    level.words.forEach(wordDef => {
      if (updatedCompletedWordIds.has(wordDef.id)) return;

      // Check if all cells in this word are locked in nextGrid
      let wordComplete = true;
      let hasLetterFromThisTurn = false;

      for (let i = 0; i < wordDef.word.length; i++) {
        const r = wordDef.direction === 'down' ? wordDef.startRow + i : wordDef.startRow;
        const c = wordDef.direction === 'right' ? wordDef.startCol + i : wordDef.startCol;
        const cell = nextGrid[r]?.[c];

        if (!cell || cell.type !== 'letter' || !cell.isLocked) {
          wordComplete = false;
          break;
        }

        if (correctPlacements.some(p => p.row === r && p.col === c)) {
          hasLetterFromThisTurn = true;
        }
      }

      if (wordComplete && hasLetterFromThisTurn) {
        updatedCompletedWordIds.add(wordDef.id);
        const bonusPoints = wordDef.word.length;
        turnScoreChange += bonusPoints;
        newlyCompletedWords.push({
          word: wordDef.displayWord || wordDef.word,
          points: bonusPoints
        });
      }
    });

    if (newlyCompletedWords.length > 0) {
      soundManager.playWordComplete();
      const firstWord = newlyCompletedWords[0];
      setWordCompleteBanner(firstWord);
      setTimeout(() => setWordCompleteBanner(null), 2400);

      // Add floating bonus on the first letter of completed word
      const targetWordDef = level.words.find(w => (w.displayWord || w.word) === firstWord.word);
      if (targetWordDef) {
        addFloatScore(targetWordDef.startRow, targetWordDef.startCol, `+${firstWord.points} BÔNUS!`, 'bonus');
      }
    }

    setCompletedWordIds(updatedCompletedWordIds);
    setGrid(nextGrid);

    // Reconstruct player's hand:
    // Remove confirmed correct letters from hand
    // Keep wrong letters in hand (as per rule: "As que estão erradas voltam para a mão do jogador")
    // Keep unplaced letters in hand
    const correctHandIndices = new Set(correctPlacements.map(p => p.handIndex));
    const currentHand = players[currentTurn].hand;
    const remainingHand = currentHand.filter((_, idx) => !correctHandIndices.has(idx));

    // Replenish current player's hand up to 5 from remainingPool
    const pool = [...remainingPool];
    const lettersNeeded = 5 - remainingHand.length;
    const drawnLetters = pool.splice(0, Math.min(lettersNeeded, pool.length));
    const updatedHand = [...remainingHand, ...drawnLetters];

    setRemainingPool(pool);

    // Update current player score and hand
    const updatedScore = Math.max(0, players[currentTurn].score + turnScoreChange);
    const updatedPlayers = {
      ...players,
      [currentTurn]: {
        ...players[currentTurn],
        score: updatedScore,
        hand: updatedHand
      }
    };
    setPlayers(updatedPlayers);

    // Clear turn placements
    setUnconfirmedPlacements([]);
    setSelectedHandIndex(null);
    setSelectedCell(null);

    // Check if all letter cells in the entire grid are locked!
    const allLetterCells = nextGrid.flatMap(r => r).filter(c => c.type === 'letter') as GridCellLetter[];
    const allLocked = allLetterCells.every(c => c.isLocked);

    if (allLocked) {
      setIsGameOver(true);
      soundManager.playWin();
      confetti({
        particleCount: 120,
        spread: 80,
        origin: { y: 0.6 }
      });

      const p1 = updatedPlayers.p1;
      const p2 = updatedPlayers.p2;
      const winner = p1.score > p2.score ? p1 : p2.score > p1.score ? p2 : 'tie';
      onGameOver?.(winner, p1, p2);
    } else {
      // Switch turn to the other player!
      setCurrentTurn(prev => (prev === 'p1' ? 'p2' : 'p1'));
    }
  };

  // Update player names
  const updatePlayerNames = useCallback((p1Name: string, p2Name: string) => {
    setPlayers(prev => {
      const nextP1 = p1Name || 'Jogador 1';
      const nextP2 = p2Name || 'Jogador 2';
      if (prev.p1.name === nextP1 && prev.p2.name === nextP2) {
        return prev;
      }
      return {
        p1: { ...prev.p1, name: nextP1 },
        p2: { ...prev.p2, name: nextP2 }
      };
    });
  }, []);

  return {
    players,
    currentTurn,
    grid,
    remainingPool,
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
  };
}
