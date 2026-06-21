import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 已知:
# - riemann_thesis-standard.md 的字节 = e6b693e5a48ce8a2abe98f8de59ba8e6959e (涓夌被鏍囨敞 UTF-8)
# - 真实 '三类标注' 的 GBK bytes = c8fdc0e0b1ead7a2  - 但这些字节在文件里根本不存在!

# 检查所有 md 文件是否"纯 ASCII" (Layer 0 code section) 中文部分还是乱码
# 也就是: 这个 md 可能根本就从来没有过真实中文
# 可能来源: 原始 md 就是英文, 中文说明被 AI 生成时就用了错误的"Google翻译"

# 试另一种方法: 用 cn_fresh_ok.md (15KB, Layer 0 缺失, 但有其他中文)
# 或者 riemann_thesis_backup_before_Replace3.md
# 或者 看 cn.html (已生成的 HTML 版本, 看看那里面有没有真实中文)

for fname in ['cn.html','cn_clean.md','riemann_thesis-standard.md']:
    p = os.path.join(r'd:\project\code\maths\黎曼猜想', fname)
    if not os.path.exists(p):
        continue
    raw = open(p,'rb').read()
    while raw.startswith(b'\xef\xbb\xbf'):
        raw = raw[3:]

    # check if raw bytes contain real Chinese UTF-8 sequence for 三类
    real_utf8_bytes = '三类'.encode('utf-8')  # e4b889e7b1bb
    has_real_sanlei = real_utf8_bytes in raw

    # check for 涓夌被 utf-8
    bad_utf8_bytes = '涓夌被'.encode('utf-8')
    has_bad = bad_utf8_bytes in raw

    print(f'{fname}: raw_has_三类_utf8_bytes={has_real_sanlei}  raw_has_涓夌被_utf8_bytes={has_bad}')

    if has_real_sanlei:
        idx = raw.find(real_utf8_bytes)
        print(f'  real context bytes: ...{raw[max(0,idx-20):idx+40].hex()}...')
        ctx = raw[max(0,idx-20):idx+40].decode('utf-8','replace')
        print(f'  real context txt: {ctx}')
