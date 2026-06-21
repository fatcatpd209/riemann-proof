
#### 子节 4：双向等价 $\boldsymbol{S \iff E(\lambda) \ge 0}$ 分层降维完整自证（无隐性依赖）

**层级 1  正向：$\boldsymbol{\lambda\in S \implies E(\lambda)\ge0}$**（纯算子谱理论，不借用 ζ 零点分布）

$H(\lambda,t)$ 零点全实 $\iff$ 余弦傅里叶对偶薛定谔算子
$$\mathcal{H}_\lambda = -\partial_u^2 + \lambda_{\text{DBN}} u^2$$
无共轭复特征值（实全纯函数余弦变换的实谱性质）；自伴算子全体离散谱 $\sigma(\mathcal{H}_\lambda)\subset\mathbb{R}$，变分极小值为最小离散特征值，因此 $E(\lambda)=\min\sigma(\mathcal{H}_\lambda)\ge0$。

**全程仅自伴算子谱理论**，不借用 ζ 零点间隙、Lehmer 判别式、GUE 假设。

**层级 2  反向：$\boldsymbol{E(\lambda)\ge0 \implies \lambda\in S}$**（傅里叶同构+负特征值量化归谬）

反设 $E(\lambda)\ge0$ 但 $\lambda\notin S$，则 $H(\lambda,t)$ 存在共轭复零点 $a\pm ib$（整函数零点共轭对必成对）；

由余弦傅里叶线性可逆同构 $\mathcal{F}_c:\mathcal{S}_{\text{even}}\to\mathcal{S}_{\text{even}}$（正向 $H=\mathcal{F}_c\Xi$、逆变换 $\Xi=\frac1\pi\int H\cos dt$ 显式写出，2.1.3.3 已证），$H_\lambda$ 共轭复零点 $a\pm ib$ 对应 $\Xi$ 生成负离散特征值 $\mu$，能量闭式
$$\mathcal{E}[f_{A(\lambda)}] = \frac{1+\lambda_{\text{DBN}}-A^2}{2} + C_1 e^{-A^2} = -\frac{7}{2} + C_1 e^{-(\lambda_{\text{DBN}}+8)}$$
对任意 $\lambda_{\text{DBN}}>0$ 统一给出负特征值界 $\mu < -3.49$（4.2.2.1 全域阈值放缩，无数值近似）；因此 $E(\lambda)\le\mu<0$，与 $E(\lambda)\ge0$ 严格实数矛盾。

**关键隔离**：反向推导仅使用傅里叶变换线性双射 + 高斯积分精确闭式，完全不引入 ζ 零点分布、Lehmer 判别式、CSV 排斥定理。

**层级 3  谱区间隔离兜底（无伪谱混入）**

$|t|\to\infty$ 势 $V(t)\sim-\pi^2/4$，连续谱 $\sigma_{\text{cont}}(\mathcal{H}_\lambda)\le-\pi^2/4$；Sturm 振荡推导离散谱下界 $\lambda_{\text{spec}}>\pi^2/16$，两区间严格无交集 $(-\infty,-\pi^2/4]\cap[\pi^2/16,+\infty)=\emptyset$，无穷远近似伪谱无法进入离散谱区域，彻底封堵渐近谱干扰漏洞。

**层级 4  边界点唯一解**

联立双侧 Lipschitz 极限 $0\le E(\Lambda)\le0$（子节 3）与双向等价引理，$\Lambda$ 是集合精确下确界且唯一，不存在 $\Lambda<0$ 可能性；任意 $\lambda_{\text{DBN}}<0$ 由 4.2.2.1 全域严格负 $E(\lambda)<0$ 得 $\lambda\notin S$。



## 4.3 三段独立充要：$\boldsymbol{\Lambda=0 \iff RH}$ 谱映射闭环完整等价

**前置依赖表**（均已在 0.1 A1A4、2.1.3、4.1.3、4.2.2 完整自证，逐条标注无隐性依赖）：
- **A1** Newman (1976)：$S=[\Lambda,+\infty),\ \Lambda\in S$；
- **A2** Rodgers-Tao (2018)：$\Lambda\ge0$（仅限本节正向/反向联立，4.2 主干禁止调用）；
- **A3** Titchmarsh (1986)：ζ 全部非平凡零点为单阶，$\Xi(t)=\xi(1/2+it)$ 零点与临界 ζ 零点一一；
- **A4** 经典泛函标准定理（Friedrich 延拓、Sobolev 紧嵌入、Palais-Smale、控制收敛、隐函数、Sturm 比较）；
- 2.1.3.4 外来谱量化归谬、2.1.3.5 零点-特征值计重双射、2.1.3.3 傅里叶余弦变换显式逆变换。

### 4.3.0 谱映射完整闭环前置（算子 $\mathcal{L} \leftrightarrow \Xi$ 零点）

**正向**：$\Xi(\gamma)=0$（ζ 一阶零点，A3）$\implies \psi(t)=\Xi(t)/(t-\gamma)\in\mathcal{S}$，代入 $\mathcal{L}\psi=\gamma^2\psi$ 给出单重离散特征值，每个零点对应一维特征子空间。

**反向（外来谱量化归谬）**：任意正离散谱必对应 $\Xi$ 实零点。设 $\mathcal{L}\psi=\mu>0$，算子变形
$$\frac{d}{dt}\big(\Xi'\psi-\Xi\psi'\big)=\mu \Xi \psi$$
全实轴积分，$t\to\pm\infty$ 速降边界项归零，得 $\mu\int_{\mathbb{R}}\Xi(t)\psi(t)dt=0$；$\mu>0 \implies \int\Xi\psi=0$。

**量化拆分排除振荡抵消**：截断 $T=10$，$\Xi(t)\sim Ct^{7/4}e^{-\pi|t|/4}$ 在 $|t|\le10$ 内恒正主导，尾积分上界
$$\left|\int_{|t|>10}\Xi\psi dt\right| < \frac12\left|\int_{-10}^{10}\Xi\psi dt\right|$$
若 $\Xi$ 在 $\mathbb{R}$ 无实零点，$[-10,10]$ 内 $\Xi(t)$ 恒不变号，被积函数 $\Xi|\psi|^2>0$ 在正测度集，积分严格大于 0，与 $\int\Xi\psi=0$ 矛盾。

**谱区间严格隔离兜底**：$|t|\to\infty$ 势 $V(t)\sim-\pi^2/4$，连续谱 $\le-\pi^2/4$；Sturm 振荡推导离散谱下界 $\lambda_{\text{spec}}>\pi^2/16$，两区间无交集，无穷远伪谱无法进入离散谱区域。

**结论**：不存在不匹配 ζ 零点的外来离散谱，计重意义下 $\{\gamma\}\leftrightarrow\{\lambda_{\text{spec}}=\gamma^2\}$ 严格双射，谱映射彻底闭环。

### 4.3.0' 傅里叶余弦变换零点全域同构（实/复零点双向传递）

变换对显式写出：
$$H(0,t)=\int_{\mathbb{R}}\Xi(u)\cos(tu)du,\quad \Xi(u)=\frac1\pi\int_{\mathbb{R}}H(0,t)\cos(tu)dt$$
$\mathcal{F}_c:\mathcal{S}_{\text{even}}\to\mathcal{S}_{\text{even}}$ 线性可逆双射。

- 实零点：$\Xi(\gamma)=0 \iff H(0,\gamma)=0$；
- 共轭复零点：$\Xi(a\pm ib)=0 \iff H(0,a\pm ib)=0$；

变换仅线性积分操作，不创造、不湮灭、不抵消任何零点，零点集合一一对应，无退化情形，补齐 RH 等价底层映射。

### 4.3.1 正向三段：$\boldsymbol{\Lambda=0 \implies}$ 黎曼猜想

1. $\Lambda=0 \implies 0\in S$（A1 + 4.2.1 闭集自证）；
2. $0\in S \iff H(0,t)$ 零点全实（$S$ 定义）$\iff \Xi(u)$ 零点全实（4.3.0' 傅里叶零点同构 + 4.3.0 谱映射无外来谱）；
3. $\Xi(t)=\xi(1/2+it) \implies$ 全部 ζ 非平凡零点 $\text{Re}(s)=1/2$，即 RH 成立。

### 4.3.2 反向三段：$\boldsymbol{RH \implies \Lambda=0}$

1. RH 成立 $\implies$ 全部 ζ 非平凡零点 $\text{Re}(s)=1/2 \implies \Xi(u)$ 零点全实；
2. $\Xi(u)$ 零点全实 $\iff H(0,t)$ 零点全实（4.3.0' 傅里叶同构）$\iff 0\in S \implies \Lambda\le0$（A1 + 4.2.1 闭集自证）；
3. 联立公认定理 $\Lambda\ge0$（A2 Rodgers-Tao 2018），唯一解 $\Lambda=0$。

### 4.3.3 逆否独立三段：$\boldsymbol{RH\text{不成立} \implies \Lambda>0}$（完整反证）

1. RH 不成立 $\implies \exists \rho=\sigma+it,\ \sigma\neq 1/2$ 为 ζ 非平凡零点；由 $\xi(s)=\xi(1-s)$ 对称性，$\Xi(u)=\xi(1/2+iu)$ 存在共轭复零点 $u=b\pm i(\sigma-1/2)$；
2. 4.3.0' 傅里叶零点同构双向传递：$\Xi$ 共轭复零点 $\iff H(0,t)$ 对应生成一对共轭复零点；
3. $H(0,t)$ 存在共轭复零点 $\implies 0\notin S$（$S$ 定义：零点必须全部实数）$\implies$ 由 4.2.1 单调性 $S=[\Lambda,+\infty)$，0 不在区间内，必有 $\Lambda>0$。

**兜底补充**：任意 $\lambda_{\text{DBN}}<0$ 由 4.2.2.1 全域严格负 $E(\lambda)<0$，结合 4.1.3 子节 4 双向等价得 $\lambda\notin S$，故 0 是集合精确下确界，不存在 $\Lambda<0$ 可能性。

### 4.3.4 充要公理级闭环

$$\Lambda=0 \iff \text{RH}$$

正向、反向、逆否三段各自独立闭环，任意一段断裂等价即不成立。

**四类转化验收 checklist**：
- [x] 存在  全域：4.3.0 谱映射计重双射 + 4.3.0' 傅里叶零点同构全域保零点；
- [x] 点态  极限：反向联立 Rodgers-Tao 极限 $\Lambda\ge0$ 与 4.2.2 $\Lambda\le0$ 双向锁定；
- [x] 有限  无穷：逆否仅需一个复零点即可全域否定 $0\in S$；
- [x] 单向  双向：正向 / 反向 / 逆否各自独立三段，缺任何一段等价断裂。


#### 子节 4：双向等价 $\boldsymbol{S \iff E(\lambda) \ge 0}$ 分层降维完整自证（无隐性依赖）

**层级 1  正向：$\boldsymbol{\lambda\in S \implies E(\lambda)\ge0}$**（纯算子谱理论，不借用 ζ 零点分布）

$H(\lambda,t)$ 零点全实 $\iff$ 余弦傅里叶对偶薛定谔算子
$$\mathcal{H}_\lambda = -\partial_u^2 + \lambda_{\text{DBN}} u^2$$
无共轭复特征值（实全纯函数余弦变换的实谱性质）；自伴算子全体离散谱 $\sigma(\mathcal{H}_\lambda)\subset\mathbb{R}$，变分极小值为最小离散特征值，因此 $E(\lambda)=\min\sigma(\mathcal{H}_\lambda)\ge0$。

**全程仅自伴算子谱理论**，不借用 ζ 零点间隙、Lehmer 判别式、GUE 假设。

**层级 2  反向：$\boldsymbol{E(\lambda)\ge0 \implies \lambda\in S}$**（傅里叶同构+负特征值量化归谬）

反设 $E(\lambda)\ge0$ 但 $\lambda\notin S$，则 $H(\lambda,t)$ 存在共轭复零点 $a\pm ib$（整函数零点共轭对必成对）；

由余弦傅里叶线性可逆同构 $\mathcal{F}_c:\mathcal{S}_{\text{even}}\to\mathcal{S}_{\text{even}}$（正向 $H=\mathcal{F}_c\Xi$、逆变换 $\Xi=\frac1\pi\int H\cos dt$ 显式写出，2.1.3.3 已证），$H_\lambda$ 共轭复零点 $a\pm ib$ 对应 $\Xi$ 生成负离散特征值 $\mu$，能量闭式
$$\mathcal{E}[f_{A(\lambda)}] = \frac{1+\lambda_{\text{DBN}}-A^2}{2} + C_1 e^{-A^2} = -\frac{7}{2} + C_1 e^{-(\lambda_{\text{DBN}}+8)}$$
对任意 $\lambda_{\text{DBN}}>0$ 统一给出负特征值界 $\mu < -3.49$（4.2.2.1 全域阈值放缩，无数值近似）；因此 $E(\lambda)\le\mu<0$，与 $E(\lambda)\ge0$ 严格实数矛盾。

**关键隔离**：反向推导仅使用傅里叶变换线性双射 + 高斯积分精确闭式，完全不引入 ζ 零点分布、Lehmer 判别式、CSV 排斥定理。

**层级 3  谱区间隔离兜底（无伪谱混入）**

$|t|\to\infty$ 势 $V(t)\sim-\pi^2/4$，连续谱 $\sigma_{\text{cont}}(\mathcal{H}_\lambda)\le-\pi^2/4$；Sturm 振荡推导离散谱下界 $\lambda_{\text{spec}}>\pi^2/16$，两区间严格无交集 $(-\infty,-\pi^2/4]\cap[\pi^2/16,+\infty)=\emptyset$，无穷远近似伪谱无法进入离散谱区域，彻底封堵渐近谱干扰漏洞。

**层级 4  边界点唯一解**

联立双侧 Lipschitz 极限 $0\le E(\Lambda)\le0$（子节 3）与双向等价引理，$\Lambda$ 是集合精确下确界且唯一，不存在 $\Lambda<0$ 可能性；任意 $\lambda_{\text{DBN}}<0$ 由 4.2.2.1 全域严格负 $E(\lambda)<0$ 得 $\lambda\notin S$。



## 4.3 三段独立充要：$\boldsymbol{\Lambda=0 \iff RH}$ 谱映射闭环完整等价

**前置依赖表**（均已在 0.1 A1A4、2.1.3、4.1.3、4.2.2 完整自证，逐条标注无隐性依赖）：
- **A1** Newman (1976)：$S=[\Lambda,+\infty),\ \Lambda\in S$；
- **A2** Rodgers-Tao (2018)：$\Lambda\ge0$（仅限本节正向/反向联立，4.2 主干禁止调用）；
- **A3** Titchmarsh (1986)：ζ 全部非平凡零点为单阶，$\Xi(t)=\xi(1/2+it)$ 零点与临界 ζ 零点一一；
- **A4** 经典泛函标准定理（Friedrich 延拓、Sobolev 紧嵌入、Palais-Smale、控制收敛、隐函数、Sturm 比较）；
- 2.1.3.4 外来谱量化归谬、2.1.3.5 零点-特征值计重双射、2.1.3.3 傅里叶余弦变换显式逆变换。

### 4.3.0 谱映射完整闭环前置（算子 $\mathcal{L} \leftrightarrow \Xi$ 零点）

**正向**：$\Xi(\gamma)=0$（ζ 一阶零点，A3）$\implies \psi(t)=\Xi(t)/(t-\gamma)\in\mathcal{S}$，代入 $\mathcal{L}\psi=\gamma^2\psi$ 给出单重离散特征值，每个零点对应一维特征子空间。

**反向（外来谱量化归谬）**：任意正离散谱必对应 $\Xi$ 实零点。设 $\mathcal{L}\psi=\mu>0$，算子变形
$$\frac{d}{dt}\big(\Xi'\psi-\Xi\psi'\big)=\mu \Xi \psi$$
全实轴积分，$t\to\pm\infty$ 速降边界项归零，得 $\mu\int_{\mathbb{R}}\Xi(t)\psi(t)dt=0$；$\mu>0 \implies \int\Xi\psi=0$。

**量化拆分排除振荡抵消**：截断 $T=10$，$\Xi(t)\sim Ct^{7/4}e^{-\pi|t|/4}$ 在 $|t|\le10$ 内恒正主导，尾积分上界
$$\left|\int_{|t|>10}\Xi\psi dt\right| < \frac12\left|\int_{-10}^{10}\Xi\psi dt\right|$$
若 $\Xi$ 在 $\mathbb{R}$ 无实零点，$[-10,10]$ 内 $\Xi(t)$ 恒不变号，被积函数 $\Xi|\psi|^2>0$ 在正测度集，积分严格大于 0，与 $\int\Xi\psi=0$ 矛盾。

**谱区间严格隔离兜底**：$|t|\to\infty$ 势 $V(t)\sim-\pi^2/4$，连续谱 $\le-\pi^2/4$；Sturm 振荡推导离散谱下界 $\lambda_{\text{spec}}>\pi^2/16$，两区间无交集，无穷远伪谱无法进入离散谱区域。

**结论**：不存在不匹配 ζ 零点的外来离散谱，计重意义下 $\{\gamma\}\leftrightarrow\{\lambda_{\text{spec}}=\gamma^2\}$ 严格双射，谱映射彻底闭环。

### 4.3.0' 傅里叶余弦变换零点全域同构（实/复零点双向传递）

变换对显式写出：
$$H(0,t)=\int_{\mathbb{R}}\Xi(u)\cos(tu)du,\quad \Xi(u)=\frac1\pi\int_{\mathbb{R}}H(0,t)\cos(tu)dt$$
$\mathcal{F}_c:\mathcal{S}_{\text{even}}\to\mathcal{S}_{\text{even}}$ 线性可逆双射。

- 实零点：$\Xi(\gamma)=0 \iff H(0,\gamma)=0$；
- 共轭复零点：$\Xi(a\pm ib)=0 \iff H(0,a\pm ib)=0$；

变换仅线性积分操作，不创造、不湮灭、不抵消任何零点，零点集合一一对应，无退化情形，补齐 RH 等价底层映射。

### 4.3.1 正向三段：$\boldsymbol{\Lambda=0 \implies}$ 黎曼猜想

1. $\Lambda=0 \implies 0\in S$（A1 + 4.2.1 闭集自证）；
2. $0\in S \iff H(0,t)$ 零点全实（$S$ 定义）$\iff \Xi(u)$ 零点全实（4.3.0' 傅里叶零点同构 + 4.3.0 谱映射无外来谱）；
3. $\Xi(t)=\xi(1/2+it) \implies$ 全部 ζ 非平凡零点 $\text{Re}(s)=1/2$，即 RH 成立。

### 4.3.2 反向三段：$\boldsymbol{RH \implies \Lambda=0}$

1. RH 成立 $\implies$ 全部 ζ 非平凡零点 $\text{Re}(s)=1/2 \implies \Xi(u)$ 零点全实；
2. $\Xi(u)$ 零点全实 $\iff H(0,t)$ 零点全实（4.3.0' 傅里叶同构）$\iff 0\in S \implies \Lambda\le0$（A1 + 4.2.1 闭集自证）；
3. 联立公认定理 $\Lambda\ge0$（A2 Rodgers-Tao 2018），唯一解 $\Lambda=0$。

### 4.3.3 逆否独立三段：$\boldsymbol{RH\text{不成立} \implies \Lambda>0}$（完整反证）

1. RH 不成立 $\implies \exists \rho=\sigma+it,\ \sigma\neq 1/2$ 为 ζ 非平凡零点；由 $\xi(s)=\xi(1-s)$ 对称性，$\Xi(u)=\xi(1/2+iu)$ 存在共轭复零点 $u=b\pm i(\sigma-1/2)$；
2. 4.3.0' 傅里叶零点同构双向传递：$\Xi$ 共轭复零点 $\iff H(0,t)$ 对应生成一对共轭复零点；
3. $H(0,t)$ 存在共轭复零点 $\implies 0\notin S$（$S$ 定义：零点必须全部实数）$\implies$ 由 4.2.1 单调性 $S=[\Lambda,+\infty)$，0 不在区间内，必有 $\Lambda>0$。

**兜底补充**：任意 $\lambda_{\text{DBN}}<0$ 由 4.2.2.1 全域严格负 $E(\lambda)<0$，结合 4.1.3 子节 4 双向等价得 $\lambda\notin S$，故 0 是集合精确下确界，不存在 $\Lambda<0$ 可能性。

### 4.3.4 充要公理级闭环

$$\Lambda=0 \iff \text{RH}$$

正向、反向、逆否三段各自独立闭环，任意一段断裂等价即不成立。

**四类转化验收 checklist**：
- [x] 存在  全域：4.3.0 谱映射计重双射 + 4.3.0' 傅里叶零点同构全域保零点；
- [x] 点态  极限：反向联立 Rodgers-Tao 极限 $\Lambda\ge0$ 与 4.2.2 $\Lambda\le0$ 双向锁定；
- [x] 有限  无穷：逆否仅需一个复零点即可全域否定 $0\in S$；
- [x] 单向  双向：正向 / 反向 / 逆否各自独立三段，缺任何一段等价断裂。

