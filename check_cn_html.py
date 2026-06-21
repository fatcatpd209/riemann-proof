import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# cn.html = 151KB pandoc 产出? 看看里面有什么
p = r'd:\project\code\maths\黎曼猜想\cn.html'
raw = open(p, 'rb').read()
while raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]

# Decode as utf-8
try:
    txt = raw.decode('utf-8')
except:
    txt = raw.decode('gb18030', errors='replace')

real_sanlei_bytes = '三类'.encode('utf-8')
has_real = real_sanlei_bytes in raw
has_layer = 'Layer 0' in txt

print(f'cn.html: size={len(txt)} bytes_real_sanlei={has_real} has_Layer0={has_layer}')

if has_real:
    idx = txt.find('三类')
    print(f'  real 三类 ctx: {txt[idx-15:idx+60]}')

if has_layer:
    idx2 = txt.find('Layer 0')
    print(f'  Layer0 ctx: {txt[idx2-15:idx2+80]}')

# Extract <pre><code> block around Layer 0
for m in re.finditer(r'Layer 0.{0,200}', txt, re.S):
    snippet = m.group(0)
    cjk = sum(1 for c in snippet if '\u4e00' <= c <= '\u9fff')
    print(f'  Layer0 match (cjk={cjk}): {snippet[:150]}')
    break
