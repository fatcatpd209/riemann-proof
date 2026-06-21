import re
with open(r'd:\project\code\maths\黎曼猜想\riemann_thesis.md','r',encoding='utf-8') as f:
    content = f.read()
end43 = content.find('## 4.4 ')
maintext = content[:end43]
print('Main text ends at:', end43)
count = 0
for m in re.finditer('Lehmer|CSV|Csordas', maintext, re.IGNORECASE):
    count += 1
    s = max(0, m.start()-50); e = min(len(maintext), m.start()+100)
    snip = maintext[s:e].replace(chr(10),' ').replace(chr(13),' ')
    print('  at', m.start(), ': [...', snip, '...]')
print('Total matches:', count)
print('---')
print('Last 300 chars of maintext:', repr(maintext[-300:]))
