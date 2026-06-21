import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

root = r'd:\project\code\maths\黎曼猜想'
for fname in ['riemann_thesis-standard.md', 'riemann_thesis_original_restored.md',
              'riemann_thesis_cn_clean.md', 'cn_fresh.md', 'cn_fresh_ok.md', 'cn_hd.md',
              'riemann_thesis1.md', 'riemann_thesis_v4_broken.md', '_work1.md']:
    p = os.path.join(root, fname)
    if not os.path.exists(p):
        continue
    raw = open(p, 'rb').read()
    found = False
    for enc in ['utf-8', 'gbk', 'gb18030', 'latin1']:
        try:
            txt = raw.decode(enc)
        except Exception:
            continue
        markers = []
        if '三类标注' in txt:
            markers.append('三类标注')
        if '涓夌被' in txt:
            markers.append('涓夌被(坏)')
        if markers:
            print(f'{fname} dec={enc}  {markers}  size={len(txt)}')
            for m in markers:
                idx = txt.find(m)
                print('  ctx:', txt[max(0,idx-25):idx+35])
            found = True
            break
    if not found:
        print(f'{fname}: NO markers  size={len(raw)}')
