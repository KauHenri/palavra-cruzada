export type PlayerId = 'p1' | 'p2';

export interface Player {
  id: PlayerId;
  name: string;
  score: number;
  hand: string[]; // up to 5 letters
  color: string;
  avatar: string;
}

export type Direction = 'right' | 'down';

export interface ClueInfo {
  text: string;
  direction: Direction;
  icon?: string | null;
}

export interface GridCellClue {
  type: 'clue';
  clues: ClueInfo[];
}

export interface GridCellLetter {
  type: 'letter';
  solution: string; // The target uppercase letter (A-Z)
  displayChar?: string; // Character with accent for display (e.g., 'Ã', 'É')
  currentLetter: string | null;
  isLocked: boolean;
  confirmedBy: PlayerId | null;
  wordIds: string[];
}

export interface GridCellEmpty {
  type: 'empty';
}

export type GridCell = GridCellClue | GridCellLetter | GridCellEmpty;

export interface WordDefinition {
  id: string;
  word: string;
  displayWord?: string;
  direction: Direction;
  startRow: number;
  startCol: number;
  clueText: string;
  clueRow: number;
  clueCol: number;
  icon?: string | null;
}

export interface LevelDefinition {
  id: number;
  title: string;
  subtitle: string;
  theme: string;
  rows: number;
  cols: number;
  grid: GridCell[][];
  words: WordDefinition[];
}

export interface PendingPlacement {
  row: number;
  col: number;
  letter: string;
  handIndex: number;
}

export interface FloatScoreNotification {
  id: string;
  row: number;
  col: number;
  text: string;
  type: 'correct' | 'wrong' | 'bonus';
}
