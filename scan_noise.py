import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'd:\project\code\maths\黎曼猜想\riemann_thesis-standard.md'
t = open(p, 'r', encoding='utf-8').read()
lines = t.split('\n')

# Print ALL section headers and surrounding context so we can identify noise
print(f'Total lines: {len(lines)}')
print()
print('=== ALL HEADINGS WITH LINE NUM ===')
for i, l in enumerate(lines, 1):
    if re.match(r'^#{1,6}\s', l):
        has_code = False
        ctx_idx = i  # 1-indexed
        j = i
        while j < len(lines) and not lines[j-1].strip().startswith('```'):
            j += 1
        if j < len(lines) and lines[j-1].strip().startswith('```'):
            has_code = True
        print(f'L{i}: {l}  [code_block_near={has_code}]')

# Also print every line that looks like AI/test noise
noise_patterns = [
    r'Added', r'Pass', r'Fail', r'OK$', r'checklist', r'验证',
    r'Phase\s*\d', r'phase\s*\d', r'\d+/\d+\s*OK', r'ring\s*workaround',
    r'附录\s*[A-E]', r'Appendix\s*[A-E]', r'DAG\s*实验', r'DAG\s*experiment',
    r'变更记录', r'commit', r'CI', r'workflow',
    r'全量编译', r'构建结果', r'31/31', r'31/31',
    r'优化点', r'整改', r'整改验证',
    r'测试经验', r'测试报告', r'验证结果',
    r'一致性总结', r'Phase\s*\d\s*完成',
]

noise_re = re.compile('|'.join(noise_patterns), re.IGNORECASE)

print('\n=== NOISE CANDIDATE LINES ===')
for i, l in enumerate(lines, 1):
    if noise_re.search(l):
        preview = l[:100]
        print(f'L{i}: {preview}')

# Also find tables with checkmarks or Pass/Added
print('\n=== PASS/Added TABLE LINES ===')
for i, l in enumerate(lines, 1):
    if ('|' in l and ('Added' in l or 'Pass' in l or '✔' in l or '✅' in l or '✓' in l)):
        print(f'L{i}: {l[:120]}')

# Find lines with emoji or checkmark unicode
print('\n=== CHECKMARK/EMOJI LINES ===')
for i, l in enumerate(lines, 1):
    for ch in l:
        if ch in ('✓','✔','✅','❌','❌','✗','🚀','📝','📊','🔬','⚙️','🧪','📋','🔧','🛠','📌','🔑','📚','🎯','📈','🧠','💡','🔍','📐','📏','🔢','📊','🎓','🧮','📝','📌','💡','🔑','📚','🎯','📈','🧠','🔬','⚙️','🧪','📋','🔧','🛠'):
            print(f'L{i} (ch={repr(ch)}): {l[:120]}')
            break
