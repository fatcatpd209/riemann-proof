import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'd:\project\code\maths\黎曼猜想\riemann_thesis-standard.md'
t = open(p, 'r', encoding='utf-8').read()
lines = t.split('\n')
# Dump raw sections with their byte offsets for segmentation
# We need to split into chunks. Let's find natural chunk boundaries.
# Chunk A: Lines 1-200 (Abstract + Layer 0 intro + Layer 0 code block start 60%)
# Chunk B: Layer 0 code block rest + Layer 0 S/R Axioms (200-400)
# Chunk C: Layer 0 rest + Layer 1-2 (400-700)
# Chunk D: Main theory (700-1000)
# Chunk E: Remainder (1000+)

boundaries = [1, 200, 400, 700, 1000, 1627]
out_dir = r'd:\project\code\maths\黎曼猜想\chunks'
os.makedirs(out_dir, exist_ok=True)
for i in range(len(boundaries)-1):
    s, e = boundaries[i], boundaries[i+1]
    chunk = '\n'.join(lines[s-1:e-1])
    fname = os.path.join(out_dir, f'chunk_{chr(ord("A")+i)}_{s}_{e-1}.md')
    open(fname, 'w', encoding='utf-8').write(chunk)
    print(f'Chunk {chr(ord("A")+i)} lines {s}-{e-1}: {len(chunk)} chars -> {fname}')

# Also write a list of boundaries for reference
ref = []
for ln, l in enumerate(lines, 1):
    if l.strip().startswith('#'):
        ref.append(f'L{ln}: {l}')
open(os.path.join(out_dir, 'HEADINGS.txt'), 'w', encoding='utf-8').write('\n'.join(ref))
print(f'\nWrote HEADINGS.txt ({len(ref)} headings)')
