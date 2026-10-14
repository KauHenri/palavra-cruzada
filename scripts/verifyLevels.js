// Helper to build and validate Swedish-style crossword levels
function buildLevel({ id, title, subtitle, theme, rows, cols, wordsData }) {
  // wordsData: array of {
  //   word: string,
  //   clue: string,
  //   direction: 'right' | 'down',
  //   startRow: number,
  //   startCol: number,
  //   icon?: string
  // }

  // Initialize empty grid
  const grid = Array.from({ length: rows }, () =>
    Array.from({ length: cols }, () => ({ type: 'empty' }))
  );

  const cluesMap = new Map(); // key: "r,c" -> list of { text, direction, icon }

  // First verify & register clues
  wordsData.forEach((w) => {
    let clueR = w.direction === 'down' ? w.startRow - 1 : w.startRow;
    let clueC = w.direction === 'right' ? w.startCol - 1 : w.startCol;

    if (w.customCluePos) {
      clueR = w.customCluePos.row;
      clueC = w.customCluePos.col;
    }

    if (clueR < 0 || clueR >= rows || clueC < 0 || clueC >= cols) {
      throw new Error(`Clue for "${w.word}" at (${clueR}, ${clueC}) is out of grid bounds (${rows}x${cols})`);
    }

    const key = `${clueR},${clueC}`;
    if (!cluesMap.has(key)) {
      cluesMap.set(key, []);
    }
    cluesMap.get(key).push({
      text: w.clue,
      direction: w.direction,
      icon: w.icon
    });
  });

  // Assign clues to grid
  for (const [key, clueList] of cluesMap.entries()) {
    const [r, c] = key.split(',').map(Number);
    grid[r][c] = {
      type: 'clue',
      clues: clueList
    };
  }

  // Populate words into grid
  const words = [];
  wordsData.forEach((w, wIdx) => {
    const cleanWord = w.word.toUpperCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    const len = cleanWord.length;
    const wordId = `w_${id}_${wIdx + 1}`;

    let clueR = w.direction === 'down' ? w.startRow - 1 : w.startRow;
    let clueC = w.direction === 'right' ? w.startCol - 1 : w.startCol;
    if (w.customCluePos) {
      clueR = w.customCluePos.row;
      clueC = w.customCluePos.col;
    }

    for (let i = 0; i < len; i++) {
      const r = w.direction === 'down' ? w.startRow + i : w.startRow;
      const c = w.direction === 'right' ? w.startCol + i : w.startCol;

      if (r >= rows || c >= cols) {
        throw new Error(`Word "${w.word}" goes out of bounds at (${r}, ${c})`);
      }

      const cell = grid[r][c];
      if (cell.type === 'clue') {
        throw new Error(`Word "${w.word}" letter '${cleanWord[i]}' collides with clue at (${r}, ${c})`);
      }

      if (cell.type === 'letter') {
        if (cell.solution !== cleanWord[i]) {
          throw new Error(`Collision at (${r}, ${c}) for "${w.word}" (letter '${cleanWord[i]}'), existing is '${cell.solution}'`);
        }
        cell.wordIds.push(wordId);
      } else {
        grid[r][c] = {
          type: 'letter',
          solution: cleanWord[i],
          displayChar: w.word[i].toUpperCase(),
          currentLetter: null,
          isLocked: false,
          confirmedBy: null,
          wordIds: [wordId]
        };
      }
    }

    words.push({
      id: wordId,
      word: cleanWord,
      direction: w.direction,
      startRow: w.startRow,
      startCol: w.startCol,
      clueText: w.clue,
      clueRow: clueR,
      clueCol: clueC
    });
  });

  let totalLetters = 0;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (grid[r][c].type === 'letter') totalLetters++;
    }
  }

  console.log(`[OK] Level ${id}: "${title} - ${subtitle}" (${rows}x${cols}) | ${words.length} palavras | ${totalLetters} letras`);
  return { id, title, subtitle, theme, rows, cols, grid, words };
}

// ----------------------------------------------------
// LEVEL 1: Aquecimento Romântico (5 rows x 6 cols)
// ----------------------------------------------------
const level1 = buildLevel({
  id: 1,
  title: "Fase 1",
  subtitle: "Aquecimento Romântico",
  theme: "Amor & Carinho",
  rows: 5,
  cols: 6,
  wordsData: [
    // Top row clues pointing down
    { word: "AMOR", clue: "Sentimento maior", direction: "down", startRow: 1, startCol: 1, icon: "❤️" },
    { word: "BOM", clue: "Oposto de ruim", direction: "down", startRow: 1, startCol: 3 },
    { word: "SOL", clue: "Aquece o dia", direction: "down", startRow: 1, startCol: 5, icon: "☀️" },

    // Left clues pointing right
    { word: "ABAS", clue: "Partes do boné", direction: "right", startRow: 1, startCol: 1 },
    { word: "MIMO", clue: "Agradinho fofo", direction: "right", startRow: 2, startCol: 1, icon: "🎁" },
    { word: "ONDA", clue: "Movimento do mar", direction: "right", startRow: 3, startCol: 1, icon: "🌊" },
    { word: "RUA", clue: "Via pública", direction: "right", startRow: 4, startCol: 1 }
  ]
});

// Let's check Level 1 letter grid:
// Row 1: (1,1)=A, (1,2)=B, (1,3)=A, (1,4)=S. But down word 2 at col 3 starts at (1,3) with 'B'.
// Wait! Let's verify if 'ABAS' has 'A' at index 2 (col 3), while 'BOM' has 'B' at row 1!
// That's why the script checks collisions!
