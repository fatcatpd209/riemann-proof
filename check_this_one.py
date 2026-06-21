import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

p = r'd:\project\code\maths\黎曼猜想\riemann_thesis-standard.md'
raw = open(p, 'rb').read()
while raw.startswith(b'\xef\xbb\xbf'):
    raw = raw[3:]
t = raw.decode('utf-8', errors='replace')

idx_layer = t.find('Layer 0')
idx_sanlei = t.find('三类')
idx_jianbei = t.find('涓夌被')

print(f'文件: riemann_thesis-standard.md')
print(f'字节大小: {len(raw)} bytes')
print(f'UTF-8 解码后字符数: {len(t)}')
print()
print(f'Layer 0 在文本里: {idx_layer >= 0}')
print(f'真实中文 三类 在文本里: {idx_sanlei >= 0}')
print(f'乱码字符 涓夌被 在文本里: {idx_jianbei >= 0}')

if idx_layer >= 0:
    layer_bytes = b'Layer 0'
    byte_idx = raw.find(layer_bytes)
    print()
    print(f'=== Layer 0 附近的原始字节 (hex) ===')
    print(raw[byte_idx-5:byte_idx+150].hex())
    print()
    print(f'=== Layer 0 附近按 UTF-8 解码 ===')
    print(raw[byte_idx-5:byte_idx+150].decode('utf-8', errors='replace'))
    print()
    print(f'=== Layer 0 上下文里的每个非ASCII字符 ===')
    ctx = t[idx_layer:idx_layer+120]
    for ch in ctx:
        if ord(ch) >= 128:
            try:
                ch.encode('gbk')
                gb_ok = 'GBK可编码'
            except Exception:
                gb_ok = 'GBK不可编码'
            print(f'  U+{ord(ch):04X} {ch!r}  UTF-8={ch.encode("utf-8").hex()}  {gb_ok}')

print()
real_bytes = '三类'.encode('utf-8')
has_real = real_bytes in raw
print(f'真实中文 "三类" 的 UTF-8 字节: {real_bytes.hex()}')
print(f'这些字节是否出现在文件里: {has_real}')
print()
real_gbk = '三类'.encode('gbk')
has_real_gbk = real_gbk in raw
print(f'真实中文 "三类" 的 GBK 字节: {real_gbk.hex()}')
print(f'这些字节是否出现在文件里: {has_real_gbk}')
