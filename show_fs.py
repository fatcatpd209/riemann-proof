import sys, io, os, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

root = r'd:\project\code\maths\黎曼猜想'
items = []
for fname in os.listdir(root):
    p = os.path.join(root, fname)
    if os.path.isfile(p):
        st = os.stat(p)
        items.append((st.st_mtime, st.st_size, fname))
items.sort(reverse=True)
for mtime, size, fname in items[:20]:
    print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(mtime))}  {size:>10,}  {fname}')
