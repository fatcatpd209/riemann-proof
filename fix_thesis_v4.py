#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

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

def replace_range(text, start_marker, end_marker, new_content, label):
    i1 = text.find(start_marker)
    if i1 < 0:
        print('WARN %s start not found: %r' % (label, start_marker[:60]))
        return text
    i2 = text.find(end_marker, i1 + len(start_marker))
    if i2 < 0:
        i2 = len(text)
    new_text = text[:i1] + new_content + '\n' + text[i2:]
    print('  Replaced %s (%d -> %d chars)' % (label, len(text), len(new_text)))
    return new_text

LATEX = r"\boldsymbol{"

# ============================================================
# 1. FIX §4.1.3
# ============================================================
s413_new = (
"### 4.1.3 De Bruijn-Newman 三类变分框架（修正版）\n\n"
"**重要修正声明**（替代原稿 §4.1.3 定义）：\n"
"原稿中 $E(\\lambda_{\\text{DBN}}) = \\inf_{\\|f\\|=1} \\int |f'|^2 + \\lambda_{\\text{DBN}} u^2 |f|^2$ 是**量子谐振子基态能量**，"
"与 DBN 零点集合 $S$ **不存在已证数学联系**（FATAL 2，2026-06-19 审查）。本小节重写为标准 DBN 文献"
"（Rodgers-Tao 2020、Polymath 2019、Csordas-Smith-Varga 1994）一致的三类变分框架。\n\n"
"**定义4.1.3.1（DBN 热流函数）**：标准定义（Rodgers-Tao 2020 eq.(1)）\n"
"$$H_t(z) = \\int_0^\\infty e^{t u^2} \\Phi(u) \\cos(zu)\\,du$$\n"
"其中 $\\Phi(u) = 4\\sum_{n=1}^\\infty \\left(2\\pi^2 n^4 e^{9u} - 3\\pi n^2 e^{5u}\\right) e^{-\\pi n^2 e^{4u}}$（超指数衰减偶函数）。\n"
"初始条件 $H_0(z) = \\frac{1}{8}\\xi\\left(\\frac{1}{2}+\\frac{iz}{2}\\right)$，即黎曼 $\\xi$ 函数的 Fourier 余弦变换。\n\n"
"**定义4.1.3.2（零点集合）**：\n"
"$$S = \\{ t \\in \\mathbb{R} \\mid H_t(z) \\text{ 的所有零点均为实数} \\}, \\quad \\Lambda = \\inf S$$\n"
"RH 等价于 $\\Lambda \\le 0$（定义恒等）。Newman 猜想是 $\\Lambda \\ge 0$（Rodgers-Tao 2020 已证）。\n\n"
"**变分框架 1：Pólya 实零判别（偶数整函数 Fourier 判据）**\n"
"Pólya 1927：若 $H(z) = \\int_0^\\infty \\Phi(u) \\cos(zu) du$ 是偶函数整函数，且 $\\Phi \\in L^1(\\mathbb{R}, (1+u^2)du)$ 满足 $\\Phi(u) \\ge 0$，"
"则 $H$ 的所有零点实当且仅当 $\\Phi$ 是**正测度的 Fourier 余弦变换**（Bochner 定理 + de Bruijn 实零判别）。"
"对 $H_t$，热因子 $e^{tu^2}$ 改写为 $\\Phi_t(u) = e^{tu^2}\\Phi_0(u)$，要求 $\\Phi_t$ 为偶正可测函数的 Fourier 余弦像。\n\n"
"**变分框架 2：Csordas-Smith-Varga Sturm-Liouville 振荡（1994）**\n"
"对任意 $z \\in \\mathbb{C}$，定义 Sturm-Liouville 微分算子：\n"
"$$\\mathcal{A}f = -f'' + Q_{t}(u)\\,f$$\n"
"其中 $Q_t(u) = -(\\Phi_t'/\\Phi_t)'(u) = \\partial_{uu}\\log |\\Phi_t(u)|$ 是 $\\Phi_t$ 诱导的势。"
"$H_t$ 所有零点实当且仅当对每个 $\\gamma \\in \\mathbb{R}$，方程 $\\mathcal{A}f = \\gamma^2 f$ 仅有实特征值"
"（Sturm 比较定理 + 振荡计数）。**注**：这不是谐振子。\n\n"
"**变分框架 3：Dobner Dirichlet 级数零点判别（2020）**\n"
"$\\zeta_t(s) = \\sum_{n=1}^\\infty \\exp\\left(\\frac{t}{4}\\log^2 n\\right) n^{-s}$。对 $t<0$，$\\zeta_t(s)$ 有无穷多零点"
"偏离临界线 $\\Re(s)=1/2$，直接证明 $t \\notin S$。Dobner 给出 Newman 猜想（$\\Lambda \\ge 0$）的全新证明。\n\n"
"**单调性（Pólya 热流定理）**：若 $H_{t_0}$ 零点全实且 $t > t_0$，则 $H_t$ 零点全实。"
"标准证明（Pólya 1935 via de Bruijn 1950）：热演化在 $\\Phi$ 侧是 Gaussian 卷积，保持 Pólya 实零条件，故 $t > t_0 \\implies t \\in S$。"
"$S = [\\Lambda, +\\infty)$ 右闭区间。\n\n"
"**重要声明**：原稿中 $E(\\lambda) = \\inf \\int |f'|^2 + \\lambda u^2 |f|^2$ 是错误路径。"
"$\\Lambda \\le 0 \\iff RH$ 是**定义级恒等**，而非独立 '证明' 的命题（见 §4.3）。\n"
)

s = replace_range(s, '### 4.1.3 能量泛函', '### 4.1.4', s413_new, '§4.1.3')

# ============================================================
# 2. FIX §4.2
# ============================================================
s42_new = (
"## 4.2 De Bruijn-Newman 常数与 RH 的等价：诚实现状\n\n"
"### 4.2.1 定义级恒等：$\\boldsymbol{\\Lambda \\le 0 \\iff RH}$\n"
"$$\\Lambda \\le 0 \\overset{\\text{定义}}{\\iff} H_0(z) = \\frac{1}{8}\\xi\\left(\\frac{1}{2}+\\frac{iz}{2}\\right) \\text{ 零点全实}"
"\\overset{\\text{定义}}{\\iff} \\xi(s) \\text{ 零点全在临界线} \\overset{\\text{定义}}{\\iff} RH$$\n"
"这是恒等式，不需要额外 '证明'。\n\n"
"### 4.2.2 已证定理（无条件）：Rodgers-Tao 2020 $\\Lambda \\ge 0$\n"
"Newman 1991 猜想 $\\Lambda \\ge 0$（RH 若真则 '仅勉强成立'）。Rodgers-Tao 2020 Forum Math Pi **无条件证明**了 $\\Lambda \\ge 0$。\n"
"- **Rodgers-Tao 证明思路**：反设 $\\Lambda < 0$，取 $t\\in(\\Lambda,0)$，分析 $H_t$ 零点动力学，推出 $H_0$ 零点满足局部算术进步分布"
"（由热流形变保持的局部平衡），与 Montgomery 对关联估计矛盾。\n"
"- **Dobner 2020 简化证明**：$\\zeta_t(s) = \\sum e^{\\frac{t}{4}\\log^2 n} n^{-s}$ 对 $t<0$ 有无穷多零点偏离临界线，直接给出 $t \\notin S$。\n"
"- Andrade-Chang-Miller 2013 构造数值下界 $\\Lambda \\ge -1.145\\times10^{-11}$。\n\n"
"### 4.2.3 已知上界：Polymath 2019 $\\Lambda \\le 0.22$\n"
"Polymath arXiv:1904.12438 结合有效数值验证 + 渐近零区域分析，给出**无条件上界** $\\Lambda \\le 0.22$；后续数值改进到 $\\Lambda \\le 0.017$。\n"
"- Andrade-Chang-Miller 2013 在函数场设置下表明，CM 曲线的 DBN 常数精确等于 $\\log |a_p(\\mathcal{D})|/(2\\sqrt{p})$，由 Sato-Tate 定理存在子列 $p_j$ 使得 $\\Lambda_{D_{p_j}} \\to 0$。\n\n"
"### 4.2.4 已知边界总结\n"
"| 结果 | 来源 | 类型 |\n|---|---|---|\n"
"| $\\Lambda \\ge 0$ | Rodgers-Tao 2020 | 无条件定理 |\n"
"| $\\Lambda \\le 0.22$ | Polymath 2019 | 无条件（含数值验证） |\n"
"| $\\Lambda \\ge -1.145\\times 10^{-11}$ | Andrade-Chang-Miller 2013 | 数值下界 |\n"
"| $\\Lambda = 0$? | — | **等价于 RH 本身** |\n\n"
"**核心结论**：证明 $\\Lambda = 0$ 与证明 RH 是同一难度的命题。当前最佳边界 $\\Lambda \\in [0, 0.22]$。\n"
)

s = replace_range(s, '## 4.2 核心原创主证明', '## 4.3', s42_new, '§4.2')

# ============================================================
# 3. FIX §4.3
# ============================================================
s43_new = (
"## 4.3 三段独立充要：$\\boldsymbol{\\Lambda = 0 \\iff RH}$（定义级等价）\n\n"
"### 4.3.1 正向 $\\boldsymbol{\\Lambda = 0 \\implies RH}$\n"
"- $\\Lambda = 0 \\implies 0 \\in S$（由 $S = [\\Lambda, +\\infty)$ 右闭区间）\n"
"- $0 \\in S \\iff H_0(z)$ 零点全实\n"
"- $H_0(z) = \\frac{1}{8}\\xi(\\frac{1}{2}+\\frac{iz}{2})$ 零点全实 $\\iff \\xi(s)$ 零点全在 $\\Re(s)=1/2 \\iff RH$\n\n"
"### 4.3.2 反向 $\\boldsymbol{RH \\implies \\Lambda = 0}$\n"
"- RH 成立 $\\implies \\xi(s)$ 零点全在临界线 $\\implies H_0(z)$ 零点全实 $\\implies 0 \\in S \\implies \\Lambda \\le 0$\n"
"- 联立 Rodgers-Tao 2020 无条件定理 $\\Lambda \\ge 0$\n"
"- 取唯一解 $\\boldsymbol{\\Lambda = 0}$\n\n"
"**诚实解释**：这不是 '证明 RH'，而是**在 RH 已成立的前提下**给出的 DBN 框架内的等价陈述。\n\n"
"### 4.3.3 逆否独立三段：$\\boldsymbol{RH\\text{不成立} \\implies \\Lambda > 0}$\n"
"- RH 不成立 $\\implies \\exists \\rho=\\sigma+it,\\ \\sigma\\neq 1/2$ 为 $\\zeta$ 非平凡零点\n"
"- 由 $\\xi(s) = \\xi(1-s)$，$\\Xi(u) = \\xi(1/2+iu)$ 有共轭复零点 $u=b\\pm i(\\sigma-1/2)$\n"
"- Pólya 实零判别给出 $0 \\notin S \\implies \\Lambda > 0$\n\n"
"### 4.3.4 诚实结论\n"
"$\\Lambda = 0$ 与 RH 是同一数学命题的不同语言。**证明 $\\Lambda = 0$ 就是证明 RH**，没有捷径。"
"DBN 框架提供了漂亮的 reformulation，但没有绕过 RH 的核心困难（证明 $\\xi$ 零点全在临界线）。\n"
)

s = replace_range(s, '## 4.3 三段独立充要', '## 4.4', s43_new, '§4.3')

# ============================================================
# 4. FIX §2.1.3
# ============================================================
s213_new = (
"### 2.1.3 Sturm-Liouville 算子谱与 DBN 零点关系（修正版）\n\n"
"原稿 §2.1.3 的 Gaussian 谐振子算子与 $\\zeta$ 零点**无已证联系**（FATAL 4）。本小节重写为 Csordas-Smith-Varga 1994 正确框架。\n\n"
"#### 2.1.3.1 DBN 势定义\n"
"$$\\Phi(u) = 4\\sum_{n=1}^\\infty \\left(2\\pi^2 n^4 e^{9u} - 3\\pi n^2 e^{5u}\\right) e^{-\\pi n^2 e^{4u}}$$\n"
"$\\Phi(u) > 0$ 对所有 $u \\in \\mathbb{R}$（正系数正项求和，Poisson theta 保证偶函数 + 正性）。热演化 $\\Phi_t(u) = e^{tu^2}\\Phi(u)$。\n\n"
"#### 2.1.3.2 Sturm-Liouville 算子\n"
"对每个 $t \\in \\mathbb{R}$，定义势函数 $Q_t(u) = -(\\Phi_t'/\\Phi_t)'(u) = \\partial_{uu}\\log |\\Phi_t(u)|$。\n"
"$$\\mathcal{A}_t\\,f = -f'' + Q_t(u)\\,f$$\n"
"**关键区别**：势 $Q_t$ 由 $\\Phi_t$ 诱导，**不是** $u^2$ 也不是 Gaussian。它是 $\\Phi$ 的对数二阶导数，与 $\\xi$ 零点分布深度耦合。\n\n"
"#### 2.1.3.3 Pólya 实零判别（Fourier 方向）\n"
"$H_t(z) = \\mathcal{F}_c \\Phi_t(z) = \\int_0^\\infty \\Phi_t(u) \\cos(zu) du$ 零点全实当且仅当 $\\Phi_t$ 是某个**正测度的 Fourier 余弦变换**"
"（Bochner 定理 + de Bruijn 1950 实零判别）。等价地，$\\Phi_t$ 必须完全凸。\n\n"
"#### 2.1.3.4 零点与 $\\zeta$ 零点的一一对应\n"
"$H_0(z) = \\frac{1}{8}\\xi(\\frac{1}{2}+\\frac{iz}{2})$ 是定义恒等。$H_0(\\gamma) = 0 \\iff \\xi(\\frac{1}{2}+i\\gamma) = 0$ 对 $\\gamma \\in \\mathbb{R}$。"
"计重双射 $\\{\\gamma \\in \\mathbb{R} \\mid H_0(\\gamma)=0\\} \\leftrightarrow \\{\\varrho \\mid \\zeta(\\varrho)=0, \\Re(\\varrho)=\\frac{1}{2}\\}$（Hadamard 乘积指数 1，单阶零点已验证前 $10^{14}$ 个）。\n\n"
"#### 2.1.3.5 Pólya 单调性\n"
"若 $t_0 \\in S$ 且 $t > t_0$，则 $t \\in S$。**正确演化**（Pólya 1935）："
"$H_{t_2}(z) = \\int_0^\\infty e^{(t_2-t_1)u^2} \\Phi_{t_1}(u) \\cos(zu) du$，**不是**原稿声称的 $e^{-\\Delta t z^2/4} H_{t_1}(z)$（FATAL 3）。\n\n"
"#### 2.1.3.6 Dobner 零点判别（反向）\n"
"对 $t < 0$，$\\zeta_t(s) = \\sum e^{\\frac{t}{4}\\log^2 n} n^{-s}$ 有无穷多零点偏离临界线。$t \\notin S$ 直接给出。\n"
)

s = replace_range(s, '### 2.1.3 算子 $\mathcal{L}$ 定义', '### 2.2 收敛域', s213_new, '§2.1.3')

# ============================================================
# 5. FIX §4.4
# ============================================================
s44_new = (
"## 4.4 后置等价推论：$\\boldsymbol{\\Lambda \\le 0 \\iff}$ 无穷多 Lehmer 对\n\n"
"**硬隔离**：本节不在主干证明链中使用。\n\n"
"**修正**：原稿 Lehmer 判别泛函 $F(\\gamma,\\gamma') < 4/5$ 是 Csordas-Smith-Varga 1994 的预施瓦茨间隔判据。"
"Rodgers-Tao 2020 恰恰利用 $t \\to 0^-$ 时零点间隙趋于 $0$ 的 Lehmer 子列来证明 $\\Lambda \\ge 0$——"
"Lehmer 对是 $\\Lambda$ 接近 $0$ 的数值征兆，而非 RH 的 '旁路' 证明。\n\n"
"### 4.4.1 定义与渐近展开\n\n"
"相邻零点 $\\gamma < \\gamma'$，$T = \\frac{\\gamma+\\gamma'}{2}$，$\\Delta = \\gamma' - \\gamma$。\n"
"$$F(\\gamma,\\gamma') = \\Delta^2 \\sum_{\\gamma_j \\notin \\{\\gamma,\\gamma'\\}} \\left( \\frac{1}{(\\gamma_j-\\gamma)^2} + \\frac{1}{(\\gamma_j-\\gamma')^2} \\right)"
" \\approx \\frac{4}{5} + \\frac{\\mathcal{I}}{\\log T}$$\n"
"$\\mathcal{I} = \\frac{1}{\\Delta}\\int_\\gamma^{\\gamma'} \\Xi''/\\Xi\\,dt$ 是预施瓦茨间隔。定义 $F < 4/5$ 为 Lehmer 对。\n\n"
"### 4.4.2 $\\boldsymbol{\\Lambda = 0 \\implies}$ 存在无穷多 Lehmer 对\n"
"若 $\\Lambda = 0$（RH 成立），零点密度 $N(T) \\sim \\frac{T}{2\\pi}\\log T$，平均间隙 $\\overline{\\Delta}(T) \\to 0$。"
"对任意大 $T_0$，存在 $T > T_0$ 使得间隙 $\\Delta < \\frac{1}{\\log T}$，代入 $F$ 渐近式得 $F < 4/5$。无穷子列 $\\{T_k\\}$ 延伸。\n\n"
"### 4.4.3 诚实反向结论\n"
"Lehmer 对存在对 $\\Lambda > 0$ 也成立（Rodgers-Tao 2020 证明 $\\Lambda \\ge 0$ 时仍有无穷多 Lehmer 对）。"
"故 $F < 4/5$ 不是 $\\Lambda \\le 0$ 的充分条件。Lehmer 对更像 $\\Lambda \\approx 0$ 的数值征兆。\n"
)

s = replace_range(s, '## 4.4 后置等价推论', '## 4.5', s44_new, '§4.4')

# ============================================================
# 6. FIX §5
# ============================================================
s5_new = (
"## 第 5 章 全域反例穷尽（修正版）\n\n"
"本章枚举 DBN 框架内可能存在的反例类型，以当前已证数学结论为基础。\n\n"
"### 5.1 反例 1：$\\boldsymbol{S \\neq [\\Lambda, +\\infty)}$\n"
"Pólya 1935 已证明单调性：若 $H_{t_0}$ 零点全实且 $t > t_0$，则 $H_t$ 零点全实。"
"$\\Lambda = \\inf S$ 有限（Newman 1976，$-\\infty < \\Lambda \\le 1/2$）。"
"$S$ 右闭（零点极限由 Hadamard 乘积 + 一致收敛给出实零点连续形变）。\n\n"
"### 5.2 反例 2：$\\boldsymbol{H_t}$ 零点分岔出复共轭对（$\\Lambda > 0$ 的原因）\n"
"**这不是反例，而是 Rodgers-Tao 证明 $\\Lambda \\ge 0$ 的核心机制**："
"$t = \\Lambda$ 处零点从实轴 '逃逸' 到上/下半复平面形成复共轭对 $\\alpha\\pm i\\beta$，$\\beta\\neq 0$。"
"分岔发生在边界 $t=\\Lambda$ 处，Pólya 单调性在 $t=\\Lambda$ 处不闭。\n\n"
"### 5.3 反例 3：$\\boldsymbol{\\Lambda > 1/2}$（de Bruijn 上界打破）\n"
"de Bruijn 1950 证明 $H_t$ 零点全实当且仅当 $t \\ge 1/2$。Polymath 2019 给出无条件上界 $\\Lambda \\le 0.22 < 1/2$。\n\n"
"### 5.4 反例 4：$\\boldsymbol{H_0}$ 零点非单阶\n"
"Gourdon 2004 验证前 $10^{14}$ 个非平凡零点单阶。多重零点最多有限个（Hadamard 乘积指数 1），不破坏等价性。\n\n"
"### 5.5 反例 5：$\\boldsymbol{\\Phi_t}$ 正性被破坏\n"
"$\\Phi(u) > 0$（逐点正系数正项和）。$\\Phi_t(u) = e^{tu^2}\\Phi(u)$ 对 $t \\ge 0$ 保持正。"
"$t < 0$ 时 $e^{tu^2}$ 对大 $|u|$ 衰减，但 $\\Phi$ 的超指数压制保证 $\\Phi_t(u)$ 对所有 $t \\in \\mathbb{R}$ 在 $u \\to \\infty$ 时仍衰减。\n\n"
"### 5.6 反例 6：$\\boldsymbol{\\Lambda}$ 数值不唯一\n"
"$\\Lambda$ 是 $S = \\{t : H_t \\text{零点全实}\\}$ 的下确界，由所有零点位置唯一确定。"
"Polymath 2019 有效渐近分析 + 有限高度 RH 验证给出上界；Dobner 2020 Dirichlet 级数给出 $\\Lambda \\ge 0$ 解析下界。\n\n"
"### 5.7 已知 '反例' 的正确解读\n"
"| 看似反例 | 实际情况 | 来源 |\n|---|---|---|\n"
"| $\\Lambda > 0$ | **定理**，已证 Rodgers-Tao 2020 | 恒成立 |\n"
"| $\\Lambda \\le 0.22$ | 无条件上界 | Polymath 2019 |\n"
"| GUE 零点关联 | Montgomery 对关联，RH 下成立 | 猜想但 RH 真则成立 |\n"
"| 函数场 $\\Lambda_{p_j} \\to 0$ | Sato-Tate + CM 曲线 DBN | Andrade-Chang-Miller 2013 |\n"
)

s = replace_range(s, '## 第 5 章', '## 6. ', s5_new, 'Ch5')

# 清理
s = ''.join(strip_emoji(c) for c in s)

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)

print('\n=== FINAL VERIFICATION ===')
print('Size:', os.path.getsize(p), 'bytes')
print('Chars:', len(s))
checks = [
    'De Bruijn-Newman 三类变分',
    'Rodgers-Tao 2020',
    'Polymath 2019',
    'Csordas-Smith-Varga',
    'Polya 实零判别',
    'Dobner 2020',
    'Lambda = 0 iff RH',
    'Lambda >= 0',
    'Lambda <= 0.22',
    'Sturm-Liouville',
    'Newman 猜想',
    '诚实结论',
    '定义级恒等',
    '谐振子',
    'Gaussian 扩散半群',
]
for kw in checks:
    ok = '  OK  ' if kw in s else '  MISS'
    print('%s %s' % (ok, kw))
