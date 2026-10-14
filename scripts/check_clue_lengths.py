import json

with open('src/data/levels.ts', 'r', encoding='utf-8') as f:
    content = f.read()

json_str = content.split('export const LEVELS: LevelDefinition[] = ')[1].rstrip(';\n')
levels = json.loads(json_str)

max_len = 0
longest_clue = None
print(f"Total levels: {len(levels)}")
for lvl in levels:
    print(f"\n=== Level {lvl['id']}: {lvl['title']} ({lvl['rows']}x{lvl['cols']}) ===")
    for w in lvl['words']:
        clue = w['clueText']
        l = len(clue)
        if l > max_len:
            max_len = l
            longest_clue = (clue, w['word'], lvl['id'])
        print(f"  {w['word']:<8} -> \"{clue}\" ({l} chars)")

print(f"\nMax clue length across entire game: {max_len} chars -> \"{longest_clue[0]}\" ({longest_clue[1]}, Level {longest_clue[2]})")
