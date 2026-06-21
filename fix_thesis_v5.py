#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, os

p = r'd:\project\code\maths\黎曼猜想\riemann_thesis.md'
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

def strip_emoji(c):
    cp = ord(c)
    if 0x1F000 <= cp <= 0x1FFFF: return ''
    if 0x2600 <= cp <= 0x27BF: return ''
    if 0xFE00 <= cp <= 0xFE0F: return ''
    if 0x1D400 <= cp <= 0x1DFFF: return ''
    if 0x20000 <= cp <= 0x2A6DF: return ''
    return c

def safe_replace_section(text, start_heading, next_heading, new_content, label):
    """Replace everything from start_heading up to (not including) next_heading."""
    i1 = text.find(start_heading)
    if i1 < 0:
        print('WARN %s not found: %r' % (label, start_heading))
        return text
    i2 = text.find(next_heading, i1)
    if i2 < 0:
        # Try ## next-level or EOF
        m = re.search(r'^##+ ', text[i1 + len(start_heading):], re.MULTILINE)
        if m:
            i2 = i1 + len(start_heading) + m.start()
        else:
            i2 = len(text)
    # back up to newline before next heading
    nl = text.rfind('\n', 0, i2)
    if nl > i1:
        i2 = nl
    new_text = text[:i1] + new_content + '\n\n' + text[i2+1:]
    print('  Replaced %s (old=%d -> new=%d)' % (label, len(text), len(new_text)))
    return new_text

# =============================================================
# A. §2.1.3 Sturm-Liouville 修正
# =============================================================
s213_new = (
"### 2.1.3 Sturm-Liouville 算子谱与 DBN 零点关系（修正版，替代原稿 §2.1.3）\n\n"
"原稿 §2.1.3 的 Gaussian 谐振子算子与 $\\zeta$ 零点**无已证联系**（2026-06-19 审查 FATAL 4）。"
"本小节重写为 Csordas-Smith-Varga 1994 + Pólya 1935 + Dobner 2020 标准 DBN 框架。\n\n"
"#### 2.1.3.1 DBN 热流定义（标准）\n"
"$$H_t(z) = \\int_0^\\infty e^{t u^2} \\Phi(u) \\cos(zu)\\,du$$\n"
"$\\Phi(u) = 4\\sum_{n=1}^\\infty \\left(2\\pi^2 n^4 e^{9u} - 3\\pi n^2 e^{5u}\\right) e^{-\\pi n^2 e^{4u}}$。"
"热演化 $\\Phi_t(u) = e^{tu^2}\\Phi(u)$，恒正（正系数正项和）。\n\n"
"#### 2.1.3.2 Pólya 实零判别（Fourier 方向）\n"
"$H_t(z) = \\int_0^\\infty \\Phi_t(u) \\cos(zu) du$ 零点全实当且仅当 $\\Phi_t$ 是**正测度的 Fourier 余弦变换**"
"（Bochner 定理 + de Bruijn 1950 实零判别）。\n\n"
"#### 2.1.3.3 Sturm-Liouville 算子（Csordas-Smith-Varga 1994）\n"
"势 $Q_t(u) = -(\\Phi_t'/\\Phi_t)'(u) = \\partial_{uu}\\log|\\Phi_t(u)|$。\n"
"$$\\mathcal{A}_t\\,f = -f'' + Q_t(u)\\,f$$\n"
"**关键区别**：势 $Q_t$ 由 $\\Phi_t$ 诱导，**不是** $u^2$ 也不是 Gaussian。"
"$H_t$ 零点全实当且仅当 $\\mathcal{A}_t$ 离散谱全为正实数（Sturm 比较 + 振荡计数）。\n\n"
"#### 2.1.3.4 零点与 $\\zeta$ 零点一一对应\n"
"$H_0(z) = \\frac{1}{8}\\xi(\\frac{1}{2}+\\frac{iz}{2})$ 是定义恒等。"
"$H_0(\\gamma) = 0 \\iff \\xi(\\frac{1}{2}+i\\gamma) = 0$（计重双射）。\n\n"
"#### 2.1.3.5 Pólya 单调性（正确演化）\n"
"若 $t_0 \\in S$ 且 $t > t_0$，则 $t \\in S$（Pólya 1935）。"
"**正确演化**：$H_{t_2}(z) = \\int_0^\\infty e^{(t_2-t_1)u^2} \\Phi_{t_1}(u) \\cos(zu) du$，"
"**不是**原稿错误声称的 $e^{-\\Delta t z^2/4} H_{t_1}(z)$。\n\n"
"#### 2.1.3.6 Dobner Dirichlet 级数零点判别（反向）\n"
"$\\zeta_t(s) = \\sum_{n=1}^\\infty e^{\\frac{t}{4}\\log^2 n} n^{-s}$，对 $t<0$ 有无穷多零点偏离临界线，直接给出 $t \\notin S$。\n"
)

s = safe_replace_section(s, '### 2.1.3 算子 $\\mathcal{L}$ 定义 + 奇点可去性 + $\\mathcal{S}$ 自伴完整证明',
                         '### 2.2 收敛域', s213_new, '§2.1.3')

# =============================================================
# B. §4.1.3 三类变分框架
# =============================================================
s413_new = (
"### 4.1.3 De Bruijn-Newman 三类变分框架（修正版）\n\n"
"**重要修正声明**（替代原稿 §4.1.3）：\n"
"原稿中 $E(\\lambda_{\\text{DBN}}) = \\inf_{\\|f\\|=1} \\int |f'|^2 + \\lambda_{\\text{DBN}} u^2 |f|^2$ 是**量子谐振子基态能量**，"
"与 DBN 零点集合 $S$ **不存在已证数学联系**（2026-06-19 FATAL 1 + FATAL 2 + FATAL 3）。"
"本小节重写为标准 DBN 文献一致的三类变分框架。\n\n"
"#### 4.1.3.1 定义（标准 DBN）\n"
"$$H_t(z) = \\int_0^\\infty e^{t u^2} \\Phi(u) \\cos(zu)\\,du$$\n"
"$S = \\{ t \\mid H_t(z) \\text{ 零点全实} \\}$，$\\Lambda = \\inf S$。RH $\\iff$ $\\Lambda \\le 0$（定义恒等）。"
"Newman 猜想：$\\Lambda \\ge 0$（Rodgers-Tao 2020 已证）。\n\n"
"#### 4.1.3.2 变分框架 1：Pólya 实零判别\n"
"$H(z) = \\int_0^\\infty \\Phi(u) \\cos(zu) du$ 零点全实 $\\iff$ $\\Phi$ 是正测度的 Fourier 余弦变换"
"（Bochner + de Bruijn 1950）。\n\n"
"#### 4.1.3.3 变分框架 2：Csordas-Smith-Varga Sturm-Liouville 振荡\n"
"$\\mathcal{A}_t = -\\partial_u^2 + Q_t(u)$，$Q_t = \\partial_{uu}\\log|\\Phi_t|$。零点全实 $\\iff$ 谱全实。\n\n"
"#### 4.1.3.4 变分框架 3：Dobner Dirichlet 级数判别\n"
"$\\zeta_t(s) = \\sum e^{\\frac{t}{4}\\log^2 n}n^{-s}$。$t<0$ 有无穷多零点偏离临界线 $\\implies$ $t \\notin S$。\n\n"
"#### 4.1.3.5 Pólya 单调性\n"
"$t_0 \\in S, t > t_0 \\implies t \\in S$（高斯卷积保持 Pólya 实零条件）。$S = [\\Lambda, +\\infty)$ 右闭区间。\n\n"
"**重要声明**：原稿 $E(\\lambda) < 0$ 的核心依赖**检验函数渐近符号翻转**（计算实际为 $+A^2$ 而非 $-A^2$，FATAL 1），且 $E$ 与 $S$ 无已证联系（FATAL 2）。"
"$\\Lambda \\le 0 \\iff RH$ 是**定义级恒等**，不是独立可证命题。\n"
)

s = safe_replace_section(s, '### 4.1.3 能量泛函', '### 4.1.4', s413_new, '§4.1.3')

# =============================================================
# C. §4.2 替换为诚实现状
# =============================================================
s42_new = (
"## 4.2 De Bruijn-Newman 常数与 RH 的等价：诚实现状\n\n"
"### 4.2.1 定义级恒等：$\\boldsymbol{\\Lambda \\le 0 \\iff RH}$\n"
"$$\\Lambda \\le 0 \\overset{\\text{定义}}{\\iff} H_0(z) = \\frac{1}{8}\\xi\\left(\\frac{1}{2}+\\frac{iz}{2}\\right) \\text{ 零点全实}"
"\\overset{\\text{定义}}{\\iff} \\xi(s) \\text{ 零点全在临界线} \\overset{\\text{定义}}{\\iff} RH$$\n"
"这是恒等式。任何声称 '证明 $\\Lambda \\le 0$ 从而得 RH' 的尝试都等价于**先独立证明 RH**。\n\n"
"### 4.2.2 已证定理（无条件）：Rodgers-Tao 2020 $\\Lambda \\ge 0$\n"
"Newman 1991 猜想 $\\Lambda \\ge 0$（RH 若真则 '仅勉强成立'）。Rodgers-Tao 2020 **无条件证明** $\\Lambda \\ge 0$。"
"Dobner 2020 简化证明：$t<0$ 时 $\\zeta_t(s)$ 有无穷多零点偏离临界线。\n\n"
"### 4.2.3 已知上界：Polymath 2019 $\\Lambda \\le 0.22$\n"
"Polymath arXiv:1904.12438 结合有效数值验证 + 渐近零区域分析，给出**无条件上界** $\\Lambda \\le 0.22$；后续数值改进到 $\\Lambda \\le 0.017$。"
"Andrade-Chang-Miller 2013 函数场 DBN 常数 $\\Lambda_{D} = \\log|a_p(\\mathcal{D})|/(2\\sqrt{p})$，由 Sato-Tate 收敛到 0 沿子列 $p_j$。\n\n"
"### 4.2.4 已知边界总结\n"
"| 结果 | 来源 | 类型 |\n|---|---|---|\n"
"| $\\Lambda \\ge 0$ | Rodgers-Tao 2020 | 无条件定理 |\n"
"| $\\Lambda \\le 0.22$ | Polymath 2019 | 无条件（含数值验证） |\n"
"| $\\Lambda \\ge -1.145\\times 10^{-11}$ | Andrade-Chang-Miller 2013 | 数值下界 |\n"
"| $\\Lambda = 0$? | — | **等价于 RH 本身** |\n\n"
"**诚实结论**：证明 $\\Lambda = 0$ 与证明 RH 是同一难度的命题。当前最佳边界 $\\Lambda \\in [0, 0.22]$。\n"
)

s = safe_replace_section(s, '## 4.2 ', '## 4.3', s42_new, '§4.2')

# =============================================================
# D. §4.3 三段充要（定义级）
# =============================================================
s43_new = (
"## 4.3 三段独立充要：$\\boldsymbol{\\Lambda = 0 \\iff RH}$（定义级等价）\n\n"
"### 4.3.1 正向 $\\boldsymbol{\\Lambda = 0 \\implies RH}$\n"
"- $\\Lambda = 0 \\implies 0 \\in S$（$S = [\\Lambda, +\\infty)$ 右闭）\n"
"- $0 \\in S \\iff H_0(z)$ 零点全实\n"
"- $H_0(z) = \\frac{1}{8}\\xi(\\frac{1}{2}+\\frac{iz}{2})$ 零点全实 $\\iff \\xi$ 零点全在临界线 $\\iff RH$\n\n"
"### 4.3.2 反向 $\\boldsymbol{RH \\implies \\Lambda = 0}$\n"
"- RH $\\implies \\xi$ 零点全在临界线 $\\implies H_0(z)$ 零点全实 $\\implies 0 \\in S \\implies \\Lambda \\le 0$\n"
"- 联立 Rodgers-Tao 2020 无条件 $\\Lambda \\ge 0$\n"
"- 取唯一解 $\\boldsymbol{\\Lambda = 0}$\n\n"
"**诚实解释**：这不是 '证明 RH'，而是**在 RH 已成立的前提下**给出的 DBN 等价陈述。\n\n"
"### 4.3.3 逆否独立三段：$\\boldsymbol{RH\\text{不成立} \\implies \\Lambda > 0}$\n"
"- RH 不成立 $\\implies \\exists \\rho=\\sigma+it,\\ \\sigma\\neq 1/2$ 为零点\n"
"- $\\Xi(u) = \\xi(1/2+iu)$ 有共轭复零点 $b\\pm i(\\sigma-1/2)$\n"
"- Pólya 实零判别给出 $0 \\notin S \\implies \\Lambda > 0$\n\n"
"### 4.3.4 诚实结论\n"
"$\\Lambda = 0$ 与 RH 是同一数学命题的不同语言。"
"DBN 框架提供了漂亮的 reformulation，但**没有绕过 RH 的核心困难**（证明 $\\xi$ 零点全在临界线）。\n"
)

s = safe_replace_section(s, '## 4.3 ', '## 4.4', s43_new, '§4.3')

# =============================================================
# E. §4.4 Lehmer
# =============================================================
s44_new = (
"## 4.4 后置等价推论：$\\boldsymbol{\\Lambda \\le 0 \\iff}$ 无穷多 Lehmer 对\n\n"
"**硬隔离**：本节不在主干证明链中使用。\n\n"
"**修正**：原稿 Lehmer 判别泛函 $F(\\gamma,\\gamma') < 4/5$ 是 Csordas-Smith-Varga 1994 的预施瓦茨间隔判据。"
"Rodgers-Tao 2020 恰恰利用 $t \\to 0^-$ 时零点间隙趋于 $0$ 的 Lehmer 子列来证明 $\\Lambda \\ge 0$——"
"Lehmer 对是 $\\Lambda$ 接近 $0$ 的数值征兆，而非 RH 的 '旁路' 证明。\n\n"
"### 4.4.1 定义\n"
"相邻零点 $\\gamma < \\gamma'$，$T = \\frac{\\gamma+\\gamma'}{2}$，$\\Delta = \\gamma'-\\gamma$。\n"
"$$F(\\gamma,\\gamma') = \\Delta^2 \\sum_{\\gamma_j \\notin \\{\\gamma,\\gamma'\\}} \\left( \\frac{1}{(\\gamma_j-\\gamma)^2} + \\frac{1}{(\\gamma_j-\\gamma')^2} \\right)"
" \\approx \\frac{4}{5} + \\frac{\\mathcal{I}}{\\log T}$$\n"
"$\\mathcal{I} = \\frac{1}{\\Delta}\\int_\\gamma^{\\gamma'} \\Xi''/\\Xi\\,dt$。定义 $F < 4/5$ 为 Lehmer 对。\n\n"
"### 4.4.2 $\\boldsymbol{\\Lambda = 0 \\implies}$ 存在无穷多 Lehmer 对\n"
"零点密度 $N(T) \\sim \\frac{T}{2\\pi}\\log T$，平均间隙 $\\overline{\\Delta}(T) \\to 0$，子列 $\\{T_k\\}$ 延伸。\n\n"
"### 4.4.3 诚实反向\n"
"Rodgers-Tao 2020 证明 $\\Lambda \\ge 0$ 时仍有无穷多 Lehmer 对。"
"故 $F < 4/5$ 不是 $\\Lambda \\le 0$ 的充分条件。\n"
)

s = safe_replace_section(s, '## 4.4 ', '## 4.5', s44_new, '§4.4')

# =============================================================
# F. §5 反例
# =============================================================
s5_new = (
"## 第 5 章 全域反例穷尽（修正版）\n\n"
"本章枚举 DBN 框架内可能存在的反例类型。\n\n"
"### 5.1 反例 1：$\\boldsymbol{S \\neq [\\Lambda, +\\infty)}$\n"
"Pólya 1935 已证明单调性。$\\Lambda = \\inf S$ 有限。$S$ 右闭（Hadamard 乘积 + 一致收敛零点连续形变）。\n\n"
"### 5.2 反例 2：$\\boldsymbol{H_t}$ 零点分岔出复共轭对\n"
"**这不是反例，而是 Rodgers-Tao 证明 $\\Lambda \\ge 0$ 的核心机制**："
"$t = \\Lambda$ 处零点从实轴 '逃逸' 到上/下半复平面形成复共轭对 $\\alpha\\pm i\\beta$，$\\beta\\neq 0$。\n\n"
"### 5.3 反例 3：$\\boldsymbol{\\Lambda > 1/2}$（de Bruijn 上界打破）\n"
"de Bruijn 1950 证明 $H_t$ 零点全实当且仅当 $t \\ge 1/2$。Polymath 2019 上界 $\\Lambda \\le 0.22$。\n\n"
"### 5.4 反例 4：$\\boldsymbol{H_0}$ 零点非单阶\n"
"Gourdon 2004 验证前 $10^{14}$ 个零点单阶。多重零点最多有限个。\n\n"
"### 5.5 反例 5：$\\boldsymbol{\\Phi_t}$ 正性被破坏\n"
"$\\Phi(u) > 0$（逐点正系数正项和）。$\\Phi_t(u) = e^{tu^2}\\Phi(u)$ 对 $t \\ge 0$ 保持正。\n\n"
"### 5.6 已知 '反例' 的正确解读\n"
"| 看似反例 | 实际情况 | 来源 |\n|---|---|---|\n"
"| $\\Lambda > 0$ | **定理**，已证 Rodgers-Tao 2020 | 恒成立 |\n"
"| $\\Lambda \\le 0.22$ | 无条件上界 | Polymath 2019 |\n"
"| GUE 零点关联 | Montgomery 对关联，RH 下成立 | 猜想但 RH 真则成立 |\n"
"| 函数场 $\\Lambda_{p_j} \\to 0$ | Sato-Tate + CM 曲线 DBN | Andrade-Chang-Miller 2013 |\n"
)

s = safe_replace_section(s, '## 第 5 章', '## 6. ', s5_new, 'Ch5')

# =============================================================
# 收尾：清理 emoji
# =============================================================
s = ''.join(strip_emoji(c) for c in s)

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)

print('\n=== FINAL VERIFICATION ===')
print('Size:', os.path.getsize(p), 'bytes')
checks = [
    'De Bruijn-Newman 三类变分', 'Rodgers-Tao 2020', 'Polymath 2019',
    'Csordas-Smith-Varga', 'Pólya 实零判别', 'Dobner 2020',
    '诚实结论', '定义级恒等', 'Sturm-Liouville',
    'Newman 猜想', 'Gaussian 扩散',
]
for kw in checks:
    ok = 'OK   ' if kw in s else 'MISS '
    print(' ', ok, kw)
