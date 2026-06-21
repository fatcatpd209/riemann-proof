#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re

p = r'd:\project\code\maths\黎曼猜想\riemann_thesis.md'
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

replacements = [
    # 全局替换原文 fake 内容为诚实版
    ('本文原创自洽引理', '**（原稿已删除）**'),
    ('本文原创不附加任何未解决数论猜想的自洽推导', '**不存在这样的无条件定理**'),
    ('本文原创变分谱推导', '**不存在的推导**'),
    ('本文原创', '**（2026-06-19 审查：原稿 FATAL 错误，已删除）**'),
    ('全程不引入、不预设、不借用', '（已删除）全程不引入、不预设、不借用'),
    ('无循环论证', '（已删除，存在循环论证风险）'),
    ('算子谱等价完整', '（已修正为 Csordas-Smith-Varga 1994）算子谱等价'),
    ('核心引理（能量泛函、谱映射）均', '已证引理（谱映射）与原稿 fake 能量泛函均'),
    ('## 4.0 主干推导公理与原创内容划分', '## 4.0 主体现状（2026-06-19 修正版）'),
    ('### 4.0.2 本文原创自洽引理（无外部猜想，全文核心创新，整套原创推导待同行评审）',
     '### 4.0.2 原稿核心创新（2026-06-19 审查发现 5 个 FATAL 错误，已重构为标准 DBN 文献框架）'),
    ('本文变分-谱框架完全兼容 Rodgers-Tao',
     '本文经重构后的标准 DBN 框架完全兼容 Rodgers-Tao'),
    ('交叉核验无逻辑矛盾', '交叉核验：原稿 fake 能量泛函与标准 DBN 理论无关（FATAL 2）'),
    ('能量泛函全域严格单调、极小可达', '（原稿）能量泛函全域严格单调、极小可达（**已删除，fat**）'),
    ('主证明独立推导 $\\Lambda\\le0$', '**原稿主证明推导 $\\Lambda\\le0$（FATAL 1-5 全部成立，已删除）**'),
    ('完整闭环证明 $\\Lambda\\le0$', '**原稿完整闭环证明 $\\Lambda\\le0$（已删除）**'),
    ('$\\Lambda\\le0$ 反证链', '**原稿 $\\Lambda\\le0$ 反证链（FATAL 1-5，已删除）**'),
    ('算子谱双向等价完整', '算子谱双向等价完整（已修正为 CSV94）'),
]

count = 0
for old, new in replacements:
    n = s.count(old)
    if n > 0:
        s = s.replace(old, new)
        count += n
        print('  %d x REPLACE: %s -> %s' % (n, old[:30], new[:30]))
    else:
        # Also try case-insensitive for common patterns
        pass

# ========= 符号表 E(lambda) 行替换（精确行）=========
i = s.find('| $E(\\lambda)$ |')
if i > 0:
    j = s.find('\n', i)
    if j < 0: j = i + 200
    s = s[:i] + '| ~~$E(\\lambda)$~~（原稿删除） | 原稿量子谐振子基态能量，与 DBN 零点集合 $S$ 无已证数学联系（FATAL 2，2026-06-19 删除） | 原稿 | FATAL 2 |' + s[j:]
    print('  REPLACE: E(lambda) table row')

# ========= 全局声明表关键修正 =========
# 找到表格行 Lambda<=0
i = s.find('$\\boldsymbol{\\Lambda \\le 0}$ |  本文原创')
if i > 0:
    j = s.find('\n', i)
    s = s[:i] + '$\\boldsymbol{\\Lambda \\le 0}$ | **不存在这样的无条件定理**（Polymath 2019 上界 $\\Lambda \\le 0.22 > 0$；Rodgers-Tao 2020 $\\Lambda \\ge 0$；联立 $\\Lambda=0$ 等价于 RH） | Polymath 2019, Dobner 2020 | 非已证 |' + s[j:]
    print('  REPLACE: Lambda<=0 table row')

# 能量泛函那行
i = s.find('| **能量泛函全域严格单调')
if i > 0:
    j = s.find('\n', i)
    s = s[:i] + '| ~~能量泛函全域严格单调、极小可达~~（已删除） | 原稿 $E(\\lambda)=\\inf \\int |f\\'|^2+\\lambda u^2|f|^2$ 是谐振子基态，恒 $>0$，不可能 $<0$（FATAL 1 算术符号翻转） | 原稿 | 2026-06-19 删除 |' + s[j:]
    print('  REPLACE: E monotonicity table')

# ========= 风险提示段修正 =========
i = s.find('** 风险提示**：本文$\\Lambda\\le0$为原创')
if i > 0:
    j = s.find('\n', i + 200)
    if j < 0: j = i + 500
    s = s[:i] + '** 风险提示**：本文 2026-06-19 审查发现 5 个 FATAL 错误：(1) 检验函数 $A^2$ 渐近符号翻转（+而非-）；(2) $E(\\lambda)$ 与 $S$ 范畴错配；(3) Gaussian 演化方向错误；(4) 算子谱映射幻觉；(5) $\\Lambda>0$ 与数值 $\\Lambda\\le 0.22$ 矛盾。整套 $\\Lambda\\le0$ 自洽推导已删除，重构为标准 DBN 文献综述（Rodgers-Tao 2020、Polymath 2019、Csordas-Smith-Varga 1994、Dobner 2020）。仅 Rodgers-Tao 2020 $\\Lambda \\ge 0$ 为公认定理。' + s[j:]
    print('  REPLACE: risk notice')

# ========= 第 10.1 成果段修正 =========
i = s.find('### 10.1 主要成果')
if i > 0:
    j = s.find('### 10.2', i)
    if j < 0: j = len(s)
    old_section = s[i:j]
    new_section = '''### 10.1 主要成果（2026-06-19 修正版）

**原稿 5 个 FATAL 错误**：
1. 检验函数渐近符号翻转（FATAL 1）：$\\mathcal{E}[f_A] \\sim (1+\\lambda)/2 + A^2$（$+\\infty$）而非原稿声称的 $-\\infty$
2. 范畴错配（FATAL 2）：$E(\\lambda) = \\inf \\int |f'|^2 + \\lambda u^2|f|^2$ 是量子谐振子基态，与 DBN 零点集合 $S$ 无已证联系
3. Gaussian 演化方向错误（FATAL 3）：$H_{t_2}(z) = \\int e^{(t_2-t_1)u^2}\\Phi_{t_1}(u)\\cos(zu)du$，不是 $e^{-\\Delta t z^2/4}H_{t_1}(z)$
4. 算子谱映射幻觉（FATAL 4）：势是 $Q_t = \\partial_{uu}\\log|\\Phi_t|$，不是 $u^2$ Gaussian
5. 数值矛盾（FATAL 5）：Polymath 2019 已证明 $\\Lambda \\le 0.22 > 0$，与 $\\Lambda \\le 0$ 矛盾

**重构后的成果**：
1. 诚实呈现 DBN 框架经典结果：Rodgers-Tao 2020 $\\Lambda \\ge 0$（无条件）、Polymath 2019 $\\Lambda \\le 0.22$（无条件）、Dobner 2020 Dirichlet 级数证明 $\\Lambda \\ge 0$
2. 三类标准 DBN 变分框架：Pólya 实零判别 + Csordas-Smith-Varga Sturm-Liouville 振荡 + Dobner Dirichlet 级数
3. 诚实结论：$\\Lambda = 0$ 与 RH 是同一命题的不同语言，不存在捷径
4. 完整列出 DBN 框架所有已发表引理及其文献来源'''
    s = s[:i] + new_section + s[j:]
    print('  REPLACE: §10.1 主要成果')

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)

print('\n=== FINAL ===')
print('Size:', os.path.getsize(p))
print('Replacements made:', count)

# 最终验证
checks = [
    ('已删除', True),
    ('FATAL', True),
    ('Rodgers-Tao 2020', True),
    ('Polymath 2019', True),
    ('Csordas-Smith-Varga', True),
    ('Dobner 2020', True),
    ('Polya 实零判别', True),
    ('定义级恒等', True),
    ('诚实结论', True),
    ('不存在的推导', True),
    ('谐振子基态', True),
    ('FATAL 1', True),
    ('FATAL 2', True),
    ('原创', True),
    ('E(\\lambda)', True),
    ('Newman (1976) | - | - |', False),  # 符号表里的旧行应该消失
]
print('\nFinal checks:')
for kw, should_exist in checks:
    if should_exist:
        ok = 'OK  ' if kw in s else 'MISS'
        print('  %s %s' % (ok, kw))
    else:
        ok = 'OK  ' if kw not in s else 'STILL PRESENT'
        print('  %s %s' % (ok, kw))
