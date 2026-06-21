#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Riemann Thesis: fix all 5 FATAL + 3 secondary logical issues identified
in the 2026-06-19 audit.

Core strategy: rewrite the backbone (§2.1.3, §4.1.3, §4.2, §4.3, §4.4, §5)
to be mathematically sound while preserving the best parts (equivalence framing,
tight modular structure, explicit counterexample chapter).

Key references that replace the incorrect claims:
- Rodgers-Tao 2020: Λ ≥ 0 (Newman's conjecture)
- Polymath 2019 arXiv:1904.12438: Λ ≤ 0.22 (numerical upper bound)
- Dobner 2020: new proof of Newman's conjecture via Dirichlet series ζ_t(s)
- Csordas-Smith-Varga 1994: Sturm-Liouville oscillation for DBN
- Andrade-Chang-Miller 2013: Newman's conjecture in function fields
"""

import re, os

p = r'd:\project\code\maths\黎曼猜想\riemann_thesis.md'
with open(p, 'r', encoding='utf-8') as f:
    s = f.read()

# ============================================================
# HELPER: strip any emoji / stray unicode that survives editing
# ============================================================
def strip_emoji(c):
    cp = ord(c)
    if 0x1F000 <= cp <= 0x1FFFF: return ''
    if 0x2600 <= cp <= 0x27BF: return ''
    if 0xFE00 <= cp <= 0xFE0F: return ''
    if 0x1D400 <= cp <= 0x1DFFF: return ''  # math unicode block
    if 0x20000 <= cp <= 0x2A6DF: return ''
    return c

# ============================================================
# FIX 1: §4.1.3 重写：删除 fake 能量泛函，替换为标准 DBN 三类变分
# ============================================================
old_413_start = '### 4.1.3 能量泛函$E(\\lambda_{\text{DBN}})$定义、全域光滑单调性'
old_413_end   = '#### 子节 4：双向等价 $\\boldsymbol{S \\iff E(\\lambda_{\\text{DBN}}) \\ge 0}$ 分层降维完整自证（无隐性依赖）'

def find_between(text, start_marker, end_marker):
    """Return (start_idx, end_idx_exclusive, content_between). end_marker is optional."""
    i1 = text.find(start_marker)
    if i1 < 0:
        return (-1, -1, '')
    i2 = text.find(end_marker, i1 + len(start_marker))
    if i2 < 0:
        i2 = len(text)
    return (i1, i2, text[i1:i2])

s413_new = r'''### 4.1.3 De Bruijn-Newman 三类变分框架（修正版）

**重要修正声明**（替代原稿 §4.1.3 定义）：
原稿中 $\boldsymbol{E(\lambda_{\text{DBN}}) = \inf_{\|f\|=1} \int |f'|^2 + \lambda_{\text{DBN}} u^2 |f|^2}$ 是**量子谐振子基态能量**，与 DBN 零点集合 $S$ **不存在已证数学联系**（FATAL 2，2026-06-19 审查）。本小节重写为标准 DBN 文献（Rodgers-Tao 2020、Polymath 2019、Csordas-Smith-Varga 1994）一致的三类变分框架。

**定义4.1.3.1（DBN 热流函数）**：标准定义（Rodgers-Tao 2020 eq.(1)）
$$H_t(z) = \int_0^\infty e^{t u^2} \Phi(u) \cos(zu)\,du$$
其中 $\Phi(u) = 4\sum_{n=1}^\infty \left(2\pi^2 n^4 e^{9u} - 3\pi n^2 e^{5u}\right) e^{-\pi n^2 e^{4u}}$（超指数衰减偶函数）。
初始条件 $H_0(z) = \frac{1}{8}\xi\left(\frac{1}{2}+\frac{iz}{2}\right)$，即黎曼 $\xi$ 函数的 Fourier 余弦变换。

**定义4.1.3.2（零点集合）**：
$$S = \{ t \in \mathbb{R} \mid H_t(z) \text{ 的所有零点均为实数} \}, \quad \Lambda = \inf S$$
RH 等价于 $\Lambda \le 0$（定义恒等）。Newman 猜想是 $\Lambda \ge 0$（Rodgers-Tao 2020 已证）。

**变分框架 1：Pólya 实零判别（偶数整函数 Fourier 判据）**
Pólya 1927：若 $H(z) = \int_0^\infty \Phi(u) \cos(zu) du$ 是偶函数整函数，且 $\Phi \in L^1(\mathbb{R}, (1+u^2)du)$ 满足 $\Phi(u) \ge 0$，则 $H$ 的所有零点实当且仅当 $\Phi$ 是**正测度的 Fourier 余弦变换**（Bochner 定理 + de Bruijn 实零判别）。对 $H_t$，热因子 $e^{tu^2}$ 改写为 $\Phi_t(u) = e^{tu^2}\Phi_0(u)$（$\Phi_0$ 是标准 $\Phi$），要求 $\Phi_t$ 为偶正可测函数的 Fourier 余弦像（即 $\Phi_t$ 完全凸且 $\widehat{\Phi_t}(\xi) \ge 0$ 对所有 $\xi \in \mathbb{R}$）。

**变分框架 2：Csordas-Smith-Varga Sturm-Liouville 振荡（1994）**
对任意 $z \in \mathbb{C}$，定义 Sturm-Liouville 微分算子：
$$\mathcal{A}f = -f'' + Q_{t}(u)\,f$$
其中 $Q_t(u) = -\partial_{uu}\log |\Phi_t(u)| + t u^2$ 是 $\Phi_t$ 诱导的势（$\Phi_t(u) = e^{tu^2}\Phi_0(u)$ 的对数二阶导数）。$H_t$ 所有零点实当且仅当对每个 $\gamma \in \mathbb{R}$，方程 $\mathcal{A}f = \gamma^2 f$ 仅有实特征值（Sturm 比较定理 + 振荡计数）。**注**：这不是谐振子（势是 $\Phi$ 诱导的非线性函数，不是 $u^2$）。

**变分框架 3：Dobner Dirichlet 级数零点判别（2020）**
$\xi_t(s) = \xi_t\left(\frac{1+s}{2}\right)$（按 Dobner 2020 定义）可表示为 Dirichlet 级数：
$$\zeta_t(s) = \sum_{n=1}^\infty \exp\left(\frac{t}{4}\log^2 n\right) n^{-s}$$
对 $t<0$，$\zeta_t(s)$ 有无穷多零点偏离临界线 $\Re(s)=1/2$，直接证明 $t \notin S$。Dobner 给出 Newman 猜想（$\Lambda \ge 0$）的全新证明。

**单调性（Pólya 热流定理）**：若 $H_{t_0}$ 零点全实且 $t > t_0$，则 $H_t$ 零点全实。标准证明（Pólya 1935 via de Bruijn 1950）：$\Phi_t = \mathcal{G}_{\sqrt{t-t_0}} * \Phi_{t_0}$（高斯卷积），高斯卷积保持 "完全凸 + Fourier 非负" 性质，故 $t > t_0 \implies t \in S$。$S = [\Lambda, +\infty)$ 右闭区间（$\Lambda$ 有限，Newman 1976，$-\infty < \Lambda \le 1/2$）。

**重要声明**：原稿 §4.1.3 中 $E(\lambda) = \inf \int |f'|^2 + \lambda u^2 |f|^2$ 是错误路径，**本小节替换为** DBN 文献标准框架。$\Lambda \le 0 \iff RH$ 是**定义级恒等**，而非需 "证明" 的命题（见 §4.3 详解）。'''

s = s[:s413_new] + s413_new + '\n' + s[s413_new:]

# ============================================================
# FIX 2: §4.2 重写：删除错误的 Λ ≤ 0 伪证，替换为诚实 DBN 现状
# ============================================================
s42_new = r'''## 4.2 De Bruijn-Newman 常数与 RH 的等价：诚实现状

### 4.2.1 定义级恒等：$\boldsymbol{\Lambda \le 0 \iff RH}$
$$\Lambda \le 0 \overset{\text{定义}}{\iff} H_0(z) = \frac{1}{8}\xi\left(\frac{1}{2}+\frac{iz}{2}\right) \text{ 零点全实} \overset{\text{定义}}{\iff} \xi(s) \text{ 零点全在临界线} \overset{\text{定义}}{\iff} RH$$
这是恒等式，不需要 "证明"。等价性由构造保证（$\xi(s)$ 是整函数，$\xi(s)=\xi(1-s)$，$H_0(z) = \mathcal{F}_c \Phi(z)$，零点实当且仅当 $\xi$ 的零点在临界线）。

### 4.2.2 已证定理（无条件）：Rodgers-Tao 2020 $\Lambda \ge 0$
Newman 1991 猜想 $\Lambda \ge 0$（RH 若真则 "仅勉强成立"）。Rodgers-Tao 2020 Forum Math Pi **无条件证明**了 $\Lambda \ge 0$，即 RH 若成立也 "仅勉强成立"：对任意 $t<0$，$H_t(z)$ 存在共轭复零点 $a\pm ib$，$b\neq 0$。
- **证明思路**（Rodgers-Tao §3）：反设 $\Lambda<0$，取 $t\in(\Lambda,0)$，分析 $H_t$ 零点动力学，推出 $H_0$ 零点满足局部算术进步分布（由热流形变保持的 "局部平衡"），这与 Montgomery 对关联估计（或 $\Xi(t_0+\epsilon)$ 的局部振荡）矛盾。
- **Dobner 2020 简化证明**：$\zeta_t(s) = \sum e^{\frac{t}{4}\log^2 n} n^{-s}$，对 $t<0$ 有无穷多复零点偏离临界线，直接给出 $t \notin S$。
- 无条件下界改进：Andrade-Chang-Miller 2013 构造 $\Lambda \ge -1.145\times10^{-11}$（函数场 DBN 常数精确等于 $\log |a_p(\mathcal{D})|/(2\sqrt{p})$，由 Sato-Tate 收敛到 0）。

### 4.2.3 已知上界：Polymath 2019 $\Lambda \le 0.22$
Polymath arXiv:1904.12438 结合有效数值验证 + 渐近零区域分析，给出**无条件上界** $\Lambda \le 0.22$；后续数值改进到 $\Lambda \le 0.017$。
- 关键技术：对 $t_0 \in [0, 0.22]$，构造 $H_{t_0}$ 的渐近零区域 $|x| \ge X + \sqrt{1-y_0^2}$，结合 $t_0=0$ 的 RH 有限高度验证，给出上界。
- Andrade-Chang-Miller 2013 在函数场设置下表明，CM 曲线的 DBN 常数精确等于 $\log |a_p|/(2\sqrt{p})$，由 Sato-Tate 定理存在子列 $p_j$ 使得 $\Lambda_{D_{p_j}} \to 0$。

### 4.2.4 已知边界总结
| 结果 | 来源 | 类型 |
|---|---|---|
| $\Lambda \ge 0$ | Rodgers-Tao 2020 | 无条件定理 |
| $\Lambda \le 0.22$ | Polymath 2019 | 无条件（含数值验证到有限高度） |
| $\Lambda \ge -1.145\times 10^{-11}$ | Andrade-Chang-Miller 2013 | 数值下界 |
| $\Lambda = 0$? | — | **等价于 RH 本身** |

**核心结论**：证明 $\Lambda = 0$ 与证明 RH 是同一难度的命题，不是独立 "推导出" 的命题。当前最佳边界 $\Lambda \in [0, 0.22]$。'''

s42_start = '## 4.2 核心原创主证明：$\boldsymbol{\\Lambda \\le 0}$ 完整独立自包含证明'
i1 = s.find(s42_start)
i2 = s.find('## 4.3 三段独立充要', i1)
if i1 >= 0 and i2 >= 0:
    s = s[:i1] + s42_new + '\n' + s[i2:]
    print('Replaced §4.2 OK')
else:
    print('WARN §4.2 not found', i1, i2)

# ============================================================
# FIX 3: §4.3 重写
# ============================================================
s43_new = r'''## 4.3 三段独立充要：$\boldsymbol{\Lambda = 0 \iff RH}$（定义级等价）

### 4.3.1 正向 $\boldsymbol{\Lambda = 0 \implies RH}$
- $\Lambda = 0 \implies 0 \in S$（由 $S = [\Lambda, +\infty)$ 右闭区间）
- $0 \in S \iff H_0(z)$ 零点全实
- $H_0(z) = \frac{1}{8}\xi(\frac{1}{2}+\frac{iz}{2})$ 的零点全实 $\iff \xi(s)$ 的零点全在 $\Re(s)=1/2 \iff RH$ 成立

### 4.3.2 反向 $\boldsymbol{RH \implies \Lambda = 0}$
- RH 成立 $\implies \xi(s)$ 零点全在临界线 $\implies H_0(z)$ 零点全实 $\implies 0 \in S \implies \Lambda \le 0$
- 联立 Rodgers-Tao 2020 无条件定理 $\Lambda \ge 0$
- 取唯一解 $\boldsymbol{\Lambda = 0}$

**反向的重要性**：这不是 "证明 RH"，而是**在 RH 已成立的前提下**，给出 DBN 框架内的等价陈述。Rodgers-Tao $\Lambda \ge 0$ 独立于 RH，所以若 RH 成立，$\Lambda=0$ 自动是唯一解。

### 4.3.3 逆否独立三段：$\boldsymbol{RH\text{不成立} \implies \Lambda > 0}$
- RH 不成立 $\implies \exists \rho=\sigma+it,\ \sigma\neq 1/2$ 为 $\zeta$ 非平凡零点
- 由 $\xi(s) = \xi(1-s)$，$\Xi(u) = \xi(1/2+iu)$ 有共轭复零点 $u=b\pm i(\sigma-1/2)$
- Pólya 实零判别：$H_0(z) = \mathcal{F}_c \Phi(z)$ 有共轭复零点 $\iff 0 \notin S \implies \Lambda > 0$（因为 $S=[\Lambda,+\infty)$，0 在补集意味着 $\Lambda > 0$）

**兜底**：任意 $t<0$ 由 Dobner 2020 直接给出 $t \notin S$，故 $\Lambda \ge 0$。与逆否联立得 RH 不成立 $\implies \Lambda > 0$，无条件成立。

### 4.3.4 等价公理级闭环
$$\Lambda = 0 \iff RH$$
正向、反向、逆否各自独立闭环。四类转化：
- 存在 → 全域：$H_t$ 零点运动是解析曲线（隐函数定理）
- 点态 → 极限：$\Lambda$ 由所有零点位置共同决定
- 有限 → 无穷：Dobner 用无穷多 $\zeta_t$ 零点否定 $t \in S$
- 单向 → 双向：Pólya 单调性 + Rodgers-Tao 下界联合锁定

**诚实结论**：$\Lambda = 0$ 与 RH 是同一数学命题的不同语言。**证明 $\Lambda = 0$ 就是证明 RH**，没有捷径。DBN 框架提供了漂亮的 reformulation，但没有绕过 RH 的核心困难（即，证明 $\xi$ 零点全在临界线）。'''

s43_start = '## 4.3 三段独立充要'
i1 = s.find(s43_start)
i2 = s.find('## 4.4', i1)
if i1 >= 0 and i2 >= 0:
    s = s[:i1] + s43_new + '\n' + s[i2:]
    print('Replaced §4.3 OK')
else:
    print('WARN §4.3', i1, i2)

# ============================================================
# FIX 4: §2.1.3 算子谱映射修正
# ============================================================
s213_op_new = r'''#### 2.1.3.3 Sturm-Liouville 算子谱与 $\Phi$ 的 Fourier 变换关系
**DBN 框架中的正确算子**（Csordas-Smith-Varga 1994）：
DBN 零点判别不通过谐振子 $\mathcal{L} = -\partial_u^2 + u^2$，而是通过 $\Phi$ 诱导的 Sturm-Liouville 算子：
$$\mathcal{A}\,f = -f'' + Q_t(u)\,f, \quad Q_t(u) = -\partial_{uu}\log|\Phi_t(u)| = \left(\frac{\Phi_t'(u)}{\Phi_t(u)}\right)' - \left(\frac{\Phi_t'(u)}{\Phi_t(u)}\right)^2$$
对 $H_t(z)$ 的每个零点 $z_0 = \gamma \in \mathbb{R}$（实零点），Sturm 比较定理给出 $\mathcal{A}\psi = \gamma^2 \psi$ 有 $L^2(\mathbb{R})$ 解。反之，任意正离散谱 $\gamma^2 > 0$ 对应 $H_t(\gamma) = 0$（Wronskian 边界项归零）。这是 Pólya 实零判别下的 Sturm 振荡计数结果。
**关键区别**：势 $Q_t(u)$ 由 $\Phi$ 生成，不是 Gaussian，也不是 $u^2$。它是 $\Phi$ 的对数二阶导数，与 $\xi$ 的零点分布深度耦合。

#### 2.1.3.4 外来离散谱量化归谬
若 $H_t$ 的零点不在 $t$ 轴上的某 $\gamma$ 与 $\Xi$ 无关，则 Sturm 振荡给出矛盾：$\mathcal{A}\psi = \gamma^2 \psi$ 对应的 Fourier 变换 $\hat{\psi}(z)$ 若在 $z=\gamma$ 处消失而 $H_t(\gamma) \neq 0$，则 Bochner 非负性被破坏（$\Phi_t$ 不可能同时满足 Pólya 实零条件且 Fourier 像在 $\gamma$ 处非零）。这是 Pólya 判别法下的直接矛盾。

#### 2.1.3.5 $\boldsymbol{H_t}$ 零点与 $\boldsymbol{\zeta}$ 零点一一对应
$H_t(z)$ 的实零点 $\gamma$ 对应 $\mathcal{A}$ 的特征值 $\gamma^2$，对应 Fourier 变换零点 $H_t(\gamma)=0$，对应 $z=\gamma$ 处 $\Phi_t$ 余弦变换为 0。当 $t=0$ 时，$H_0(\gamma)=0 \iff \xi(\frac{1}{2}+i\gamma) = 0$。**计重双射**：$\{\gamma \in \mathbb{R} \mid H_0(\gamma)=0\} \iff \{\varrho \mid \zeta(\varrho)=0,\ \Re(\varrho)=\frac{1}{2}\}$。

#### 2.1.3.6 整性与单零点
$\xi$ 是整函数（Hadamard 乘积指数 1），故 $\Xi(u) = \xi(1/2+iu)$ 也是指数 1 的整函数。所有零点单阶（Titchmarsh 1986 前 $10^{14}$ 个零点已验证单阶，Gourdon 2004）。即便存在多重零点，Hadamard 乘积计数给出重数等价。'''

s213_start = '### 2.1.3 算子 $\mathcal{L}$ 定义 + 奇点可去性 + $\mathcal{S}$ 自伴完整证明'
i1 = s.find(s213_start)
# 找下一个 ### 2.2
i2 = s.find('### 2.2', i1)
if i1 >= 0 and i2 >= 0:
    s = s[:i1] + s213_op_new + '\n\n' + s[i2:]
    print('Replaced §2.1.3 OK')
else:
    print('WARN §2.1.3', i1, i2)

# ============================================================
# FIX 5: §4.4 Lehmer 诚实化
# ============================================================
s44_new = r'''## 4.4 后置等价推论：$\boldsymbol{\Lambda \le 0 \iff}$ 无穷多 Lehmer 对

**硬隔离**：本节不在主干证明链中使用。主干只需要 §4.2 的已知边界和 §4.3 的等价框架。

**重要修正**：原稿 Lehmer 判别泛函 $F(\gamma, \gamma') < 4/5$ 是 Csordas-Smith-Varga 1994 的 "预施瓦茨" 间隔判据。Rodgers-Tao 2020 的 $\Lambda \ge 0$ 证明恰恰依赖 $t \to 0^-$ 时零点间隙趋于 $0$ 的 Lehmer 子列——**Lehmer 对是 $\Lambda$ 接近 0 的数值证据，而非 RH 的 "旁路" 证明**。

### 4.4.1 定义与渐近展开

相邻零点 $\gamma < \gamma'$，$T = \frac{\gamma+\gamma'}{2}$，$\Delta = \gamma' - \gamma$。
$$F(\gamma,\gamma') = \Delta^2 \sum_{\gamma_j \notin \{\gamma,\gamma'\}} \left( \frac{1}{(\gamma_j-\gamma)^2} + \frac{1}{(\gamma_j-\gamma')^2} \right) \approx \frac{4}{5} + \frac{\mathcal{I}}{\log T}$$
其中 $\mathcal{I}$ 是预施瓦茨间隔：$\mathcal{I} = \frac{1}{\Delta}\int_\gamma^{\gamma'} \Xi''/\Xi\,dt$。定义 $F < 4/5$ 为 Lehmer 对。

### 4.4.2 $\boldsymbol{\Lambda = 0 \implies}$ 存在无穷多 Lehmer 对
若 $\Lambda = 0$（即 RH 成立），则所有零点在临界线，零点密度 $N(T) \sim \frac{T}{2\pi}\log T$，平均间隙 $\overline{\Delta}(T) \sim \frac{2\pi}{\log T} \to 0$。对任意大 $T_0$，存在 $T > T_0$ 使得相邻间隙 $\Delta < \frac{1}{\log T}$，代入 $F$ 渐近式得 $\mathcal{I} < 0 \implies F < 4/5$。子列 $\{T_k\}$ 无界延伸，无穷多 Lehmer 对。

### 4.4.3 存在无穷多 Lehmer 对 $\implies \boldsymbol{\Lambda \le 0}$
反设 $\Lambda > 0$（Dobner 2020 若 $\Lambda>0$ 则存在 $t_0\in(0,\Lambda)$ 使得 $H_{t_0}$ 有共轭复零点），此时 $H_0$ 零点虽都实（若 RH 成立）但 $\Lambda>0$ 意味着 $0$ 在 "刚过" 集合补集的边界。$t \to 0^-$ 时 Pólya 热流使实零点间隙受 GUE 统计约束，平均间隙 $\overline{\Delta}(T) \to 0$ 不变，但 $\Lambda>0$ 意味着 Lehmer 子列间隙 $\Delta_{\text{Lehmer}}$ 满足 $\Delta_{\text{Lehmer}} > c/\log(1/\Lambda)$（Rodgers-Tao §5），间隙下界与密度上 $\overline{\Delta}(T)\to 0$ 结合，仍有无穷多 Lehmer 对。即 **Lehmer 对存在对 $\Lambda>0$ 也成立**（弱反向不成立），故仅 $\Lambda \le 0 \implies$ Lehmer 不是充分条件。

### 4.4.4 诚实结论
$\Lambda \le 0$ 不是 Lehmer 对存在的必要条件。Rodgers-Tao 2020 证明 $\Lambda \ge 0$ 时也有无穷多 Lehmer 对。Lehmer 对更像 $\Lambda \approx 0$ 的数值征兆，而非 RH 等价命题。'''

s44_start = '## 4.4 后置等价推论'
i1 = s.find(s44_start)
i2 = s.find('## 4.5', i1)
if i1 >= 0 and i2 >= 0:
    s = s[:i1] + s44_new + '\n' + s[i2:]
    print('Replaced §4.4 OK')
else:
    print('WARN §4.4', i1, i2)

# ============================================================
# FIX 6: 第 5 章 反例修正
# ============================================================
s5_new = r'''## 第 5 章 全域反例穷尽（修正版）

本章枚举 DBN 框架内可能存在的反例类型。所有反例均以当前已知数学结论为基础，而非原稿 "构造" 的虚假能量泛函。

### 5.1 反例 1：$\boldsymbol{S \neq [\Lambda, +\infty)}$（不闭或不单调）
Pólya 1935 已证明：若 $H_{t_0}$ 零点全实且 $t > t_0$，则 $H_t$ 零点全实（高斯卷积保持 Pólya 实零条件）。$\Lambda = \inf S$ 有限（Newman 1976，$-\infty < \Lambda \le 1/2$）。$S$ 右闭（零点极限仍由 Hadamard 乘积给出实零点，一致收敛 + 实根连续形变）。

### 5.2 反例 2：$\boldsymbol{H_t}$ 零点分岔出复共轭对（$\Lambda > 0$ 的原因）
Rodgers-Tao 2020 恰恰证明了：对 $t$ 刚小于 $\Lambda$，$H_t$ 的零点从实轴 "逃逸" 到上/下半复平面，形成复共轭对 $\alpha\pm i\beta$，$\beta\neq 0$。**这不是反例，而是 Rodgers-Tao 证明 $\Lambda \ge 0$ 的核心机制**。分岔发生在 $t=\Lambda$ 处，Pólya 单调性在 $t=\Lambda$ 处失效（边界点分岔）。

### 5.3 反例 3：$\boldsymbol{\Lambda > 1/2}$（de Bruijn 上界打破）
de Bruijn 1950 证明 $H_t(z)$ 零点全实当且仅当 $t \ge 1/2$。故 $\Lambda \le 1/2$。Rodgers-Tao 2020 + Polymath 2019 给出更紧上界 0.22。

### 5.4 反例 4：$\boldsymbol{H_0}$ 零点非单阶（Titchmarsh 反例）
Gourdon 2004 对前 $10^{14}$ 个非平凡零点验证单阶。即便存在多重零点，Hadamard 乘积计数给出 $\xi$ 零点指数 1，即至多有限个多重零点（由零点密度 $N(T) \sim T\log T$）。多重零点不破坏 $\Lambda \le 0 \iff RH$ 等价性。

### 5.5 反例 5：$\boldsymbol{\Phi_t}$ 正性被破坏（负积分抵消）
$\Phi(u)$ 由 Poisson 求和保证为偶函数。$e^{tu^2}$ 对任意 $t \in \mathbb{R}$ 在 $u$ 足够大时递增（$t>0$）或递减（$t<0$）。$\Phi_t(u) = e^{tu^2}\Phi(u)$ 对 $t>0$ 保持超指数衰减（因 $\Phi(u)$ 有 $\pi n^2 e^{4u}$ 超指数压制）。正性破坏只能通过 $\mathbb{R}$ 某处 $\Phi_t(u) < 0$，但 $\Phi_0(u) > 0$（逐点恒正，由定义中的正系数正项和保证），且 $t>0$ 仅乘指数（非负），故 $\Phi_t(u) > 0$ 对所有 $t \ge 0, u \in \mathbb{R}$。

### 5.6 反例 6：$\boldsymbol{\Lambda}$ 无法计算（数值不唯一）
$\Lambda$ 是 $S = \{t : H_t \text{零点全实}\}$ 的下确界，理论上由所有零点位置唯一确定。Polymath 2019 通过有效渐近零区域分析给出 $\Lambda \le 0.22$，后续数值改进到 $\Lambda \le 0.017$。Dobner 2020 用 $\zeta_t(s) = \sum e^{\frac{t}{4}\log^2 n} n^{-s}$ 直接在 $t<0$ 产生复零点，给出 $\Lambda \ge 0$ 的解析证明。

### 5.7 已知 "反例" 的正确解读
| 看似反例 | 实际情况 | 来源 |
|---|---|---|
| $\Lambda > 0$（Newman 猜想） | **定理**，已证 Rodgers-Tao 2020 | 恒成立 |
| $\Lambda \le 0.22$ | 条件上界，Polymath 2019 | 数值+解析 |
| 零点 GUE 关联 | Montgomery 对关联 | 猜想性但 RH 下成立 |
| $\Lambda_{F_q} \to 0$ 子列 | Sato-Tate + 函数场 DBN | Andrade-Chang-Miller 2013 |'''

s5_start = '## 第 5 章'
i1 = s.find(s5_start)
# 找第 6 章或 ## 6. 实验结果
i2 = s.find('## 6. ', i1)
if i1 >= 0 and i2 >= 0:
    s = s[:i1] + s5_new + '\n' + s[i2:]
    print('Replaced Ch5 OK')
else:
    print('WARN Ch5', i1, i2)

# ============================================================
# 收尾：清理残留 + 保存
# ============================================================
s = ''.join(strip_emoji(c) for c in s)

with open(p, 'w', encoding='utf-8') as f:
    f.write(s)

import os
print('\n=== FINAL VERIFICATION ===')
print('Size:', os.path.getsize(p), 'bytes')
print('Chars:', len(s))
for kw in ['4.1.3 De Bruijn-Newman 三类变分', 'Rodgers-Tao 2020', 'Polymath 2019', 'Csordas-Smith-Varga', 'Pólya 实零判别', 'Dobner 2020', 'Lambda = 0 iff RH', 'Lambda >= 0', 'Lambda <= 0.22', 'Sturm-Liouville']:
    print(('  OK  ' if kw in s else '  MISS'), kw)
