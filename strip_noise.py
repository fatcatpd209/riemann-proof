import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def strip_noise(in_path, out_path, lang='zh'):
    t = open(in_path, 'r', encoding='utf-8').read()
    lines = t.split('\n')

    # ===== STRATEGY =====
    # 1. Mark section headings -> identify ranges
    # 2. For each section, decide KEEP vs DROP
    # 3. Within kept sections, clean line-level noise

    headings = []
    for i, l in enumerate(lines, 1):
        m = re.match(r'^(#{1,6})\s+(.*)', l)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            headings.append((i, level, title))

    DROP_KEYWORDS = [
        '附录 A', '附录 B', '附录 C', '附录 D', '附录 E',
        'Appendix A', 'Appendix B', 'Appendix C', 'Appendix D', 'Appendix E',
        'Phase 4', 'Phase 5', 'Phase 6', 'phase 4', 'phase 5', 'phase 6',
        '更新记录', '一致性总结', '变更记录', '调试经验', '测试报告',
        'DAG 校验', 'dag_verify', 'ring workaround', 'ring ',
        '全量编译', '31/31', 'Pass', 'Added', 'Fail', 'Success',
        '优化点', '整改', '构建结果', '流水线', 'CI ', 'GitHub Actions',
        'workflow', 'commit',
        'Coq 9.0',
        'Phase',
    ]

    def should_drop_section(title):
        t = title.lower()
        for kw in DROP_KEYWORDS:
            if kw.lower() in t:
                return True
        return False

    # Build ranges [start_line, end_line) where DROP
    drop_ranges = []
    for hi, (ln, level, title) in enumerate(headings):
        if should_drop_section(title):
            if hi + 1 < len(headings):
                end_ln = headings[hi+1][0]
            else:
                end_ln = len(lines) + 1
            drop_ranges.append((ln, end_ln))

    print(f'Section ranges to DROP:')
    for s, e in drop_ranges:
        print(f'  L{s}-L{e-1}')

    def in_drop_range(ln):
        for s, e in drop_ranges:
            if s <= ln < e:
                return True
        return False

    # Now filter lines
    out_lines = []
    for i, l in enumerate(lines, 1):
        if in_drop_range(i):
            continue
        # Line-level cleanup even in kept sections
        cleaned = l
        # Remove [OK] CI status lines
        cleaned = re.sub(r'^\[OK\]\s*', '', cleaned)
        cleaned = re.sub(r'^\[PASS\]\s*', '', cleaned)
        cleaned = re.sub(r'^\[FAIL\]\s*', '', cleaned)
        # Remove emoji markers ✔ ✅ ❌ (but keep plain text)
        cleaned = cleaned.replace('✔', '[OK]').replace('✅', '[OK]').replace('❌', '[X]').replace('❌', '[X]')
        # Remove GitHub CI-style build metadata
        if re.match(r'^\s*(run_id:|workflow:|triggered by|commit:|branch:|sha:|artifact:)', cleaned, re.IGNORECASE):
            continue
        # Remove lines that are purely CI output noise
        if re.match(r'^\s*<details>', cleaned) or re.match(r'^\s*</details>', cleaned):
            continue
        if re.match(r'^\s*<!--', cleaned) or re.match(r'^\s*-->', cleaned):
            continue
        # Skip empty lines immediately following drop
        out_lines.append(cleaned)

    # Collapse 3+ consecutive blank lines
    collapsed = []
    blank_run = 0
    for l in out_lines:
        if l.strip() == '':
            blank_run += 1
            if blank_run <= 2:
                collapsed.append(l)
        else:
            blank_run = 0
            collapsed.append(l)

    result = '\n'.join(collapsed)
    open(out_path, 'w', encoding='utf-8').write(result)

    orig = len(t)
    new = len(result)
    removed = orig - new
    print(f'\n{lang}: {orig} chars -> {new} chars (removed {removed})')
    return result

# ============ RUN ON BOTH ============
root = r'd:\project\code\maths\黎曼猜想'
zh_in = os.path.join(root, 'riemann_thesis-standard.md')
zh_out = os.path.join(root, 'riemann_thesis_cn_clean.md')
en_in = os.path.join(root, 'riemann_thesis_en_full.md')
en_out = os.path.join(root, 'riemann_thesis_en_clean.md')

strip_noise(zh_in, zh_out, 'ZH')
strip_noise(en_in, en_out, 'EN')

print(f'\nClean files:')
print(f'  CN: {zh_out}')
print(f'  EN: {en_out}')

# Verify no noise keywords remain
for label, path in [('CN', zh_out), ('EN', en_out)]:
    t = open(path, 'r', encoding='utf-8').read()
    for kw in ['附录 A', 'Phase 4', 'Phase 5', 'Phase 6', 'DAG 校验', 'ring workaround', '31/31', 'Pass', 'Added']:
        if kw in t:
            print(f'  {label}: still has "{kw}" -> count={t.count(kw)}')
print('Clean verification done')
