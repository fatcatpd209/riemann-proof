import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

real = '三类标注'
gbk_bytes = real.encode('gbk')
print('gbk bytes:', gbk_bytes.hex())
try:
    wrong = gbk_bytes.decode('utf-8')
    print('wrong decode as utf-8:', repr(wrong))
except Exception as e:
    print('utf-8 decode fail:', e)

print('real utf-8 bytes:', real.encode('utf-8').hex())

bad = '涓夌被鏍囨敞'
bad_bytes = bad.encode('utf-8')
print('bad utf-8 bytes:', bad_bytes.hex())

try:
    real_back = bad_bytes.decode('gbk')
    print('decode as gbk:', repr(real_back))
except Exception as e:
    print('gbk fail:', e)

try:
    real_back = bad_bytes.decode('gb18030')
    print('decode as gb18030:', repr(real_back))
except Exception as e:
    print('gb18030 fail:', e)
