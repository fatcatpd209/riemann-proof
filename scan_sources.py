import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

root = r'd:\project\code\maths\黎曼猜想'

# 检查哪些 md 文件里有 "Layer 0" 代码段
for fname in os.listdir(root):
    if not fname.endswith('.md'):
        continue
    p = os.path.join(root, fname)
    raw = open(p, 'rb').read()
    while raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]
    t = raw.decode('utf-8', errors='replace')
    has_layer = 'Layer 0' in t or 'Layer0' in t
    has_coq = '```coq' in t or '```' in t
    has_sanlei = '\u4e09\u7c7b' in t
    cjk = sum(1 for c in t if '\u4e00' <= c <= '\u9fff')
    # only print big ones
    if has_layer or (cjk > 5000 and has_coq):
        idx = t.find('Layer 0')
        ctx = t[idx:idx+60] if idx >= 0 else '(no Layer 0)'
        print(f'{fname}: Layer={has_layer} coq={has_coq} sanlei={has_sanlei} cjk={cjk} size={len(t)}')
        if idx >= 0:
            print(f'  ctx: {ctx}')
