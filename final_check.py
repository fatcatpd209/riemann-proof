import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

p = r'd:\project\code\maths\黎曼猜想\riemann_thesis-standard.md'
t = open(p, 'r', encoding='utf-8').read()

idx = t.find('Layer 0')
if idx >= 0:
    print('=== Layer 0 context (all CJK chars shown as U+XXXX) ===')
    for c in t[idx:idx+500]:
        if ord(c) < 128:
            sys.stdout.write(c)
        else:
            sys.stdout.write('\\u{%04X}' % ord(c))
    sys.stdout.write('\n')

# Count real Chinese chars
real_cjk = sum(1 for c in t if 0x4E00 <= ord(c) <= 0x9FFF)
gb2312_extra = sum(1 for c in t if 0x3400 <= ord(c) <= 0x4DBF or 0xA000 <= ord(c) <= 0xA4CF or 0x20000 <= ord(c) <= 0x2A6DF)
print(f'\nReal CJK chars (U+4E00..U+9FFF): {real_cjk}')
print(f'CJK ext A/B chars: {gb2312_extra}')
print(f'Total chars: {len(t)}')

# Find if any char is in "garbled" range (U+0080..U+03FF or U+FFFD replacement)
# Real common Chinese chars should be in U+4E00..U+9FFF
bad_range1 = sum(1 for c in t if 0x0080 <= ord(c) <= 0x03FF and ord(c) not in (0x2018,0x2019,0x201C,0x201D,0x2026))
replacement = sum(1 for c in t if ord(c) == 0xFFFD)
print(f'Likely-garbled range (U+0080..U+03FF non-punct): {bad_range1}')
print(f'Replacement chars (U+FFFD): {replacement}')
