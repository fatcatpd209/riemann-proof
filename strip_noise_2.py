import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def double_strip(in_path, out_path):
    t = open(in_path, 'r', encoding='utf-8').read()
    lines = t.split('\n')
    out = []
    
    # Aggressive line-level noise removal
    for l in lines:
        stripped = l.strip()
        # Pure CI/validation rows (tables or standalone)
        if re.match(r'^\|\s*(Pass|Added|Fail|Success|OK)\s*\|', stripped, re.IGNORECASE):
            continue
        if re.match(r'^\|\s*\[?\d+/\d+\]?\s*\|', stripped):  # like | 31/31 OK |
            continue
        # Table rows with Pass/Added in them that are clearly CI validation
        if 'Added' in l and l.strip().startswith('|') and ('✓' in l or '✅' in l):
            continue
        # Emoji checkmark-only lines
        if re.match(r'^\s*[✔✅❌✗]\s*$', l):
            continue
        # Pure metadata lines
        if re.match(r'^---$', stripped) and len(out) > 0 and out[-1].strip() == '':
            # skip trailing/leading hr separators
            continue
        # Lines with "Phase N" that are purely dev-notes (not math content)
        if re.search(r'Phase\s*[4-6]', l, re.IGNORECASE):
            if not re.search(r'Phase\s*[4-6].*(Evans|Friedrich|Rellich|S-Axiom|R-Axiom|Poincare|Riemann|zeta|DBN|Palais)', l, re.IGNORECASE):
                # Skip Phase N references that don't connect to math
                continue
        # Explicit CI test output
        if re.search(r'(Run ID:|Triggered by:|workflow_|GitHub CI|pull request|check_verify|dag_verify)', l, re.IGNORECASE):
            continue
        # Full-width bracket 校验 lines
        if re.search(r'(形式化状态|Coq 处理方式|验证结果|构建结果)', l):
            if l.strip().startswith('|'):
                continue

        # For EN versions - more aggressive
        # Table row with "Pass" or "Added" or emoji in first column
        m = re.match(r'^\|\s*(.+?)\s*\|\s*(.+?)\s*\|', l)
        if m:
            col1, col2 = m.group(1), m.group(2)
            if re.search(r'(Pass|Added|Fail|✅|✔)', col1, re.IGNORECASE) or re.search(r'(Pass|Added|Fail|✅|✔)', col2, re.IGNORECASE):
                # Check all columns
                cells = [c.strip() for c in l.split('|')[1:-1]]
                if any(re.search(r'(Pass|Added|Fail|✅|✔)', c, re.IGNORECASE) for c in cells):
                    # Only skip if the table row is validation/checklist (not math theorem)
                    # Check if row contains mostly ASCII + CI keywords, no math symbols or theorem keywords
                    math_keywords = ['Theorem', 'Lemma', 'Proposition', 'Proof', 'Definition', 'Axiom', '引理', '定理', '证明']
                    if not any(mw in l for mw in math_keywords):
                        # Check if it's a validation row by looking at all cells
                        # If any cell is exactly Pass/Added/Fail or has checkmark emoji, skip
                        if any(re.fullmatch(r'(Pass|Added|Fail|Success|OK)', c, re.IGNORECASE) or
                               re.search(r'[✅✔❌✗]', c)
                               for c in cells):
                            continue

        out.append(l)

    # Collapse blank lines more aggressively
    result = []
    blank_run = 0
    for l in out:
        if l.strip() == '':
            blank_run += 1
            if blank_run <= 1:
                result.append(l)
        else:
            blank_run = 0
            result.append(l)

    final = '\n'.join(result)
    open(out_path, 'w', encoding='utf-8').write(final)
    print(f'{in_path}: {len(t)} -> {len(final)} chars (still removed {len(t)-len(final)})')
    return final

root = r'd:\project\code\maths\黎曼猜想'
zh = double_strip(os.path.join(root, 'riemann_thesis_cn_clean.md'), os.path.join(root, 'riemann_thesis_cn_final.md'))
en = double_strip(os.path.join(root, 'riemann_thesis_en_clean.md'), os.path.join(root, 'riemann_thesis_en_final.md'))

# Final check
for label, t in [('CN', zh), ('EN', en)]:
    for kw in ['附录 A', 'Pass', 'Added', 'Phase 4', 'Phase 5', 'Phase 6', 'DAG 校验', '31/31', 'ring workaround']:
        if kw in t:
            c = t.count(kw)
            print(f'  {label}: still has "{kw}" x {c}')
    print(f'  {label}: final chars = {len(t)}')
