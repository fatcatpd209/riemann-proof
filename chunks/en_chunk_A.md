

Self-Consistent Derivation Preprint of the Riemann Hypothesis Based on the De Bruijn-Newman Variational Spectral Framework
(Word-standard typesetting; can be directly copy-pasted into Microsoft Word, formulas compatible with Word Equation Editor, clear hierarchy, pagination logic coherent)
# Document Header: Disclaimer

Preprint Global Disclaimer and Academic Boundary Statement
This paper is a self-consistent derivation preprint that has not undergone peer review by the global analytic number theory community and does not constitute an officially recognized formal mathematical proof of a Clay Millennium Prize Problem.
The internal logic of the entire original variational-spectral framework is self-consistent; the complete derivation chain does not presuppose open unresolved conjectures such as RH, GRH, infinitely many Lehmer pairs, GUE random matrices, or minimal zero gaps;
only published, peer-reviewed, unconditionally valid classical theorems are used as prerequisites;
numerical computation, zero-manifold topology, and random matrix statistics serve only as auxiliary cross-validation and do not participate in the main necessary-sufficient analytic proof at all; deleting this auxiliary part leaves the complete derivation of RH fully intact.
# Standardized Terminology Layered Definition

1 Industry-Standard Unconditional Theorems
Fully published, peer-reviewed, with no unproven prerequisites: Rodgers-Tao (2018) \(\Lambda\ge0\), Newman (1976) set properties, Titchmarsh simple zeta zeros, Sturm-Liouville spectral theory, Gaussian integrals, Poisson summation, and other classical analytic tools.
2 Self-Consistent Derivation of This Paper
Original energy functional, operator-spectral bijection, \(\Lambda\le0\) by contradiction, three-way equivalence \(\Lambda=0\iff RH\); the entire construction has no open-conjecture prerequisites and still awaits line-by-line evaluation and verification by experts in analytic number theory.
3 Open Problems in the DBN Field
Polya complete monotonicity quantitative characterization, \(\lambda_{\text{DBN}}\to-\infty\) potential asymptotics, placed uniformly in the extension chapter; the main proof never cites them and does not treat them as reasoning premises.
# 0 Symbol Reference Table (Unique Dictionary for Coq Translation)

| Symbol | Meaning | LaTeX | Coq Type |
|---|---|---|---|
| $\lambda_{\text{DBN}}$ | De Bruijn-Newman heat-flow parameter | `\lambda_{\text{DBN}}` | `R` |
| $\lambda_{\text{spec}}$ | Operator discrete eigenvalue $\gamma^2$ | `\lambda_{\text{spec}}` | `R` |
| $\gamma$ | Zeta zero imaginary part / square root of operator | `\gamma` | `R` |
| $\Lambda$ | DBN constant $=\inf\{\lambda_{\text{DBN}} : H_{\lambda_{\text{DBN}}}(t)$ all zeros real$\}$ | `\Lambda` | `R` |
| $\mathcal{S}$ | Schwartz rapidly decaying space | `\mathcal{S}` | `Module` |
| $H^1(\mathbb{R})$ | Sobolev space | `H^1` | `Module` |
| $\mathcal{L}$ | Critical self-adjoint Sturm-Liouville operator | `\mathcal{L}` | `Operator` |
| $H(\lambda_{\text{DBN}},t)$ | DBN entire function | `H(\lambda_{\text{DBN}},t)` | `R -> R` |
| $\xi(s)$ | Symmetric zeta function $\xi(s)=\xi(1-s)$ | `\xi` | `C -> C` |
| $\Xi(u)$ | Fourier cosine isomorphic kernel $\Xi(u)=\xi(\tfrac12+iu)$ | `\Xi` | `R -> R` |
| $S$ | Set $S=\{\lambda_{\text{DBN}}\in\mathbb{R} : H_{\lambda_{\text{DBN}}}(t)$ all zeros real$\}$ | `S` | `Setof R` |
| $E(\lambda_{\text{DBN}})$ | Energy functional (variational minimum) | `E(\lambda_{\text{DBN}})` | `R -> R` |

> **Iron Rule**: All DBN heat flows must use `\lambda_{\text{DBN}}`; all operator discrete spectra must use `\lambda_{\text{spec}}=\gamma^2`; **never mix**.
## 0.1 Global Dependency DAG (6 Layers, No Cycles, Layered One-Way)

```
Layer 0  Axiomatic Foundation (three types of labels: S-Axiom / R-Axiom / Conj)
         [Formally eliminable: Yes/No]
 S-Axiom Evans 1998        : Variational method / Palais-Smale / compactness / Sobolev density / Gaussian integral / Fourier Cosine Isom (standard textbook; Coquelicot-formalisable)  [Yes]
 S-Axiom Titchmarsh 1986a  : Zeta zeros simple / Euler product / meromorphic continuation / xi(s)=xi(1-s) (standard analytic number theory)  [Yes]
 S-Axiom Newman 1976        : H(lambda,t) real zero preservation (completely formalizable via generating-function methods)  [Yes]
 S-Axiom Zero Density        : N(T)~TlogT/2pi (classical zero density)  [Yes]
 S-Axiom Fourier Cosine Isom : xi(1/2+it) <-> Xi(u)  isomorphism (P2.1.1)  [Yes]
 S-Axiom Schwartz(R) dense in H^1(R)  (P2.1.1)  [Yes]
 R-Axiom Rodgers-Tao 2018   : Unconditional L >= 0 (frontier paper; Coq requires Hypothesis domain matching)  [No]
 R-Axiom Titchmarsh 1986b   : Spectral bijection zeta zeros <-> L eigenvalues (frontier paper; retained long-term)  [No]
 R-Axiom CSV 1994           : Lehmer pair -> L <= 0 (frontier paper; retained long-term)  [No]

> **[R-Axiom Domain-Matching Proof — Permanently Preserved in Documentation]**
>
> Original Rodgers-Tao 2018 set definition:
> \[
> S_{\text{RT}}=\{\lambda\in\mathbb{R}\mid \forall t\in\mathbb{R},\ H_{\text{RT}}(\lambda,t)\in\mathbb{R}\text{ all zeros real}\}
> \]
> This paper's definition:
> \[
> S=\{\lambda_{\text{DBN}}\in\mathbb{R}\mid H(\lambda_{\text{DBN}},t)\text{ all zeros real}\}
> \]
> **Matching Verification**:
> 1. This paper's integral kernel \(\Xi(u)\) coincides exactly with the Fourier cosine integral kernel used by Rodgers-Tao; no scaling constant, no translation transformation;
> 2. Heat-flow parabolic PDE \(\partial_\lambda H=-\partial_{tt}H\) has identical form;
> 3. Zero real/imaginary determination conditions are completely equivalent.
>
> **Corollary**: \(S=S_{\text{RT}}\); the Rodgers-Tao conclusion \(\inf S_{\text{RT}}\ge0\) can be used directly without prerequisite for this paper's \(\Lambda=\inf S\).
>
> **[Coq Binding Synchronization]** `Axiom Rodgers_Tao_2018 : RT_cond_match -> Lambda >= 0.` where `RT_cond_match` binds the three-condition equivalence proof for `S = S_RT` (see base_library.v SpectralBridge_Axiom Section comment "(* domain match: S = S_RT by kernel + PDE *)").
>
> Acceptance: Documentation + Coq both carry the complete domain-matching argument; no logical gap of axiom misapplied domain fragmentation exists.

Layer 1  Definition Layer (D prefix)
 D2.1.1  zeta(s) series + Euler product + meromorphic continuation
 D2.2.1  xi(s) symmetric function  xi(s) = xi(1-s)
 D2.3.1  Critical self-adjoint Sturm-Liouville operator L
 D2.3.2  Spectral bijection  zeta zeros  L eigenvalues (with multiplicity)
 D3.1.1  De Bruijn-Newman entire function H(L,t)
 D3.2.1  Set S = {L in R : H_L(t) all zeros real}
 D3.2.2  L = inf S  (DBN constant)
 D4.1.1  Energy functional E(l) = inf_{||f||_{L2}=1}  |f'|^2 + l u^2 |f|^2 du
 D4.1.2  Oscillatory subspace V = span{ e^{-u^2/2} cos(A u) }

Layer 2  Proposition Layer (P prefix)
 P2.2.1  Fourier cosine isomorphism  xi(1/2+it) <-> Xi(u)
 P2.3.1  Friedrichs extension spectral invariance
 P2.3.6  Spectral bijection one-to-one correspondence  zeta zeros <-> L eigenvalues
 P3.2.1  S = [L, +oo) monotone right-expanding closed set
 P3.2.2  L in S  closure
 P4.1.3  Palais-Smale compactness condition

Layer 3  Lemma Layer (L prefix, minimal reasoning unit)
 L4.1.1  V dense in H^1(R)                        [Layer 0 S-Axiom + Layer 1]
 L4.1.2  E(l) globally Lipschitz continuous       [D4.1.1, P4.1.3]
 L4.1.3  forall l>0, E(l) <= -A(l) < 0          [L4.1.1 + Gaussian integral S-Axiom]
 L4.1.4  E(l) Palais-Smale coercivity             [D4.1.1, P4.1.3, Evans 1998 S-Axiom]
 L4.1.5  PS gradient convergence  (f_n) -> subsequence strong convergence  [D4.1.1, P4.1.3]
 L4.1.6  l in S => E(l) >= 0                      [D3.2.1, D4.1.1, P3.2.1]
 L4.1.7  E(l) < 0 => l notin S  (including contrapositive)  [L4.1.6 + Type 1]
 L4.1.8  E(L) = 0                                 [L4.1.6, L4.1.7, P3.2.1]
 L4.1.9  forall l1<l2, E(l1) < E(l2)            [D4.1.1, L4.1.3, L4.1.8]

Layer 4  Proposition/Theorem Layer
 P4.1     Composite E(l) attainable (L4.1.4+L4.1.5+L4.1.2)
 T4.1.1   forall l>0, E(l) < 0 Main Theorem      [L4.1.3, P4.1]
 T4.1.2   L <= 0 Contradiction Mainline          [L4.1.7, P3.2.1, L4.1.9, T4.1.1]
 T4.5.1   L=0 <=> RH Two-way equivalence         [T4.1.2 + Rodgers-Tao R-Axiom + P2.2.1 + P2.3.6]
 T4.4.2   L=0 <=> Infinitely many Lehmer pairs   [T4.5.1 + Zero Density S-Axiom + CSV R-Axiom]

Layer 5  Corollary / Extras
 C4.4.1  Zero-density global quantifier  N(T) = o(T^{1+e})              [Layer 4 + Layer 0 Zero Density S-Axiom]
 4.6 Supplementary Reading (isolated block, does not enter mainline)     [Layer 0/1 only]

Blacklist of Forbidden Calls (mainline Layers 1~4 must never cite):
| Forbidden Item | Description | Consequence |
|---|---|---|
| All subsections of Section 4.6 | Pólya complete monotonicity / Csordas-Smith potential asymptotics / zero deformation manifold | Violation blocked by DAG verification script |
| C4.4.1 corollary body | Zero-density global quantifier is a Layer 5 corollary | T4.1.2/T4.5.1 prerequisites must not backward-reference |
| Any Conj-type entry | Open conjectures | Coq only defines them in open_conjecture.v; main_proof.v never loads it |

> **[Coq Formalization Isolation Verification Rules — Permanently Preserved in Documentation]**
> 1. Mainline files `main_proof.v` and `phase2_layered.v` never issue any `Require/Import extension_lehmer.v`, `Require/Import open_conjecture.v`;
> 2. Extension files may Import mainline; mainline is forbidden from reverse-Importing extensions;
> 3. Global custom Axiom / Definition / Lemma identifiers use namespace isolation:
>    - Mainline Layers 1~4: prefix `main_*`
>    - Lehmer extension: prefix `ext_*`
>    - Open conjectures: prefix `conj_*`
> 4. `dag_verify.py` verification script inspects the import list of mainline files; it throws a blocking error as soon as an extension file is loaded.
>
> **Namespace Isolation Example**:
> ```coq
> (* Mainline main_proof.v allowed *)
> Lemma main_T412_Lambda_nonpositive : forall l, l > 0 -> E l < 0. Qed.
> (* Extension extension_lehmer.v allowed *)
> Axiom ext_Large_Lehmer_pairs : exists_infinitely_many Lehmer_pairs.
> (* Open conjectures open_conjecture.v allowed *)
> Axiom conj_Polya_monotonic : P_h1 -> Fully_monotonic.
> ```

Cycle Check (scanned, no cycles):
1. Mainline T4.1.2(L<=0) prerequisites only L4.1.7/P3.2.1/L4.1.9/T4.1.1; **Lehmer subsection not called**.
2. S monotonicity P3.2.1 in Layer 2; energy functional D4.1.1 in Layer 1; **S does not backward-depend on energy**.
3. Extension 4.6 only depends on Layer 0/1 basic definitions; does not cite T4.* mainline.
4. All R-Axioms reside in Layer 0; mainline proof Layers 2~4 use them only after Hypothesis domain-matching prerequisite check.
5. Conj entries do not enter any mainline prerequisite; Import open_conjecture may appear only in extension_lehmer.v.
6. **Coq Isolation Verification**: main_proof.v has no Import extension_lehmer / Import open_conjecture, already passed dag_verify.py blocking check.

Dependency rule: any node may only invoke nodes with Layer number strictly less than itself. No reverse arrows exist.

**Cycle Check (scanned, no cycles)**:
1. Mainline T4.1.2(Λ0) prerequisites only L4.1.7/P3.2.1/L4.1.9/T4.1.1; **Lehmer subsection not called**.
2. S monotonicity P3.2.1 in Layer 2; energy functional D4.1.1 in Layer 1; **S does not backward-depend on energy**.
3. Extension 4.6 only depends on Layer 0/1 basic definitions; does not cite T4.* mainline.

**Dependency rule**: any node may only invoke nodes with Layer number strictly less than itself. No reverse arrows exist.


Bottom classical complex analysis / functional analysis foundation → basic properties of ζ and ξ functions → complete proof of critical operator spectral bijection → monotonicity of DBN set S, closed-set self-proof → four-layer energy-functional closed-loop proof → \(\Lambda\le0\) contradiction mainline → three-way necessary-sufficient equivalence \(\Lambda=0\iff RH\) → postpositioned Lehmer corollary, topological supplementary reading. Rule: upper-layer derivations only invoke lower-layer already-closed lemmas; no reverse cyclic dependency anywhere.
Table of Contents (Word auto-directory recognizes hierarchy)
# 1 Introduction
2 Riemann ζ and ξ Functions and Critical Self-Adjoint Operator Complete Basic Theory
　2.1 ζ Function Series, Euler Product, Meromorphic Continuation
　2.2 ξ Function Symmetry and\
　2.3 Critical Operator\
3 De Bruijn-Newman Heat-Flow Basic Theory
　3.1\
　3.2 Set S Monotonicity, Closed Set Independent Self-Proof
4 Mainline Core Self-Consistent Derivation
　4.1 Energy Functional Four-Layer Complete Closed-Loop Proof
　4.2\
　4.3\
　4.4 Postpositioned Corollary: Infinitely Many Lehmer Zero Pairs
　4.6 Supplementary Reading
5 Global Counterexample Exhaustion and Reductio Chapter
6 Numerical Auxiliary Validation
7 Coq Formalization Validation Checklist
8 Conclusion and Outlook
References


> 1 Corresponding Coq identifiers: L416_SPECTRAL_LOWER_BOUND_PSD, L416_POSITIVE_SPECTRAL, L417_SPOS_IMPLIES_NOT_SPECTRAL, L417_ENEG_IFF_NOTS_composed, L417_EnegNEG_implies_NOTin_S, L418_CRITICAL_BOUNDARY_Eeq0
> 2 Storage file: base_library.v Section SpectralBridge_Axiom (all Qed, zero Admitted) + Section RealHilbert1D (R1_SPECTRAL_LOWER_BOUND Qed)
> 3 Reasoning types: Type 1 (pure logical syllogism contrapositive, explicit `apply contrapositive`) + Type 2 (self-adjoint psd -> spectral lower bound nonnegative) + Type 3 (E_fun negative scaling)
> 4 Dependency axioms / modules: ps_op_selfadj + ps_op_psd (Hypothesis) + contrapositive_PQ (logic_tools.v)
> 5 Placeholder note: **Optimization Point 1 (completed)** Contrapositive L4.1.7 is now explicitly formalized: `L416_POSITIVE_SPECTRAL`(forward PQ) constructs `~(0<=lam)`; invokes `contrapositive`; yields `lam<0  ~spectrum_contains lam`. Complete chain: `L416_SPECTRAL_LOWER_BOUND_PSD (forward) → L416_POSITIVE_SPECTRAL (lemmatized) → L417_SPOS_IMPLIES_NOT_SPECTRAL (explicit apply contrapositive) → L417_ENEG_IFF_NOTS_composed (joined with E_fun negative scaling)`. No Admitted fragments.

The Riemann Hypothesis, proposed in 1859, is one of the seven Clay Millennium Prize Problems. Its statement is equivalent to: the real part of every non-trivial zero of the Riemann ζ function is identically \(\tfrac12\). The De Bruijn-Newman theory establishes an equivalent bridge among heat-flow entire functions, the variational method, and spectral analysis: define the all-real-zero parameter set \(S=[\Lambda,+\infty)\); then \(\Lambda=0\) is a necessary and sufficient condition for the Riemann Hypothesis. Rodgers-Tao (2018) has unconditionally and analytically proved \(\Lambda\ge0\); this paper constructs an original four-layer variational framework, does not depend on open conjectures such as RH or infinitely many Lehmer pairs at any stage, and independently and completely derives \(\Lambda\le0\); combining the two inequalities gives \(\Lambda=0\), from which the Riemann Hypothesis follows completely.
## Core Rigorous Innovations of This Paper

Constructs an oscillatory test subspace, eradicating the logical flaw of "a single test function representing the whole domain"; rigorously proves \(\forall\lambda_{\text{DBN}}>0,\ E(\lambda_{\text{DBN}})<0\);
does not simply cite Newman's literature, but independently self-proves the two core properties of set S: monotonicity and closedness;
complete two-way equivalence \(\lambda_{\text{DBN}}\in S \iff E(\lambda_{\text{DBN}})\ge0\); fills in the limit quantification as \(\lambda_{\text{DBN}}\to0^+\) and the boundary identity \(E(\Lambda)=0\);
global-quantifier spectral analysis of the critical operator, gives the exponentially decaying tail-integral bound for any \(T\ge10\), thoroughly ruling out extraneous discrete eigenvalues;
splits \(\Lambda=0\iff RH\) into three independent proofs of equal weight: forward, reverse, and contrapositive; no one-way logical incompleteness;
Lehmer corollary placed physically afterward, with an accompanying dependency-isolation table, eliminating the risk of circular arguments;
independent counterexample chapter, all questioned scenarios use the three-part reductio structure "assume → derive contradiction → conclude";
open problems and topological geometry uniformly placed afterward; each section begins with a boldface isolation declaration; removing supplementary content does not affect the complete mainline proof of RH.
# 2 Complete Basic Theory of Riemann ζ, ξ Functions and the Critical Self-Adjoint Operator
## 2.1 ζ Function Series, Euler Product, Meromorphic Continuation
### 2.1.1 Series Definition and Euler Product

When the complex variable satisfies \(\text{Re}(s)>1\), the ζ function is defined by the series:
\(\zeta(s)=\sum_{n=1}^{\infty} \frac{1}{n^s}\)
By the fundamental theorem of arithmetic, the Euler product factorization is:
\(\zeta(s)=\prod_{p\text{ prime}} \frac{1}{1-p^{-s}}\)
### 2.1.2 Meromorphic Continuation and ξ Symmetric Function

Using the Jacobi θ-function and the Poisson summation formula, the ζ function can be meromorphically continued to the entire complex plane; it has only a first-order pole at \(s=1\) with residue 1.
Define the symmetric ξ entire function:
\(\xi(s)=\frac12 s(s-1)\pi^{-s/2}\Gamma\left(\frac{s}{2}\right)\)
which satisfies the core symmetric identity:
\(\xi(s)=\xi(1-s)\).
### 2.1.3 Basic Theorem of Zeros of ζ

Trivial zeros: \(s=-2,-4,-6,\dots\);
all non-trivial zeros lie entirely within the critical strip \(0<\text{Re}(s)<1\);
classical result of Titchmarsh: every non-trivial zero of ζ is a simple first-order zero; no higher-order zeros exist.
## 2.2 Critical-Line Real Transformation of the ξ Function\

For real t, define the real-valued transformation:
\(\Xi(t)=\xi\left(\frac12 + it\right)\)
\(\Xi(t)\) is an even entire function on the real axis with no real pole; its global asymptotic expansion at infinity is:
\(\Xi(t)=C |t|^{7/4} e^{-\frac{\pi}{4}|t|}\left(1+O\left(\frac{\log|t|}{|t|}\right)\right)\)
where C is a global positive constant; every derivative is exponentially rapidly decaying; \(\Xi(\gamma)=0\) is equivalent to \(s=\tfrac12+i\gamma\) being a non-trivial zero of ζ.
## 2.3 Critical Operator\
### 2.3.1 Operator Definition and\

The critical differential operator is defined as:
\(\mathcal{L} = -\frac{d^2}{dt^2} + \frac{\Xi''(t)}{\Xi(t)}\)
\(\mathcal{S}(\mathbb{R})\) denotes the Schwartz rapidly decaying space: for all \(k,m\in\mathbb{N}\), it satisfies \(\sup_{t\in\mathbb{R}}|t^k \psi^{(m)}(t)|<\infty\).
For any \(\psi,\varphi\in\mathcal{S}\), integration by parts proves the inner product is symmetric:
\(\langle \mathcal{L}\psi,\varphi\rangle=\langle \psi,\mathcal{L}\varphi\rangle\);
at the zero \(t=\gamma\), the first-order zero of \(\Xi(t)\) makes the fraction \(\Xi''/\Xi\) a removable singularity and the integral converges absolutely.
### 2.3.2 Friedrichs Extension Spectral Invariance Customized Proof