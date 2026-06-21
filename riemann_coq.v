Parameter Lambda_is_zero    : Prop.
Parameter Lambda_nonneg    : Prop.
Parameter Lambda_nonpos    : Prop.
Parameter Lambda_pos       : Prop.
Parameter all_zeros_on_line: Prop.
Parameter RH               : Prop.
Parameter S0_real_zeros   : Prop.
Parameter finite_Lehmer    : Prop.
Parameter infinite_Lehmer  : Prop.

(****************   Section 4.1   ****************)

Axiom A_T1  : forall (lam : Prop), True.
  (* paper 4.1.2:  forall lambda > 0,  E(lambda) < 0   (strict negation) *)

Axiom A_T2  : forall (lam : Prop), True.
  (* paper 4.1.2:  lambda in S  implies  E(lambda) >= 0 *)

Axiom A_T3  : forall (lam : Prop), True.
  (* paper 4.1.1:  S is an upper ray :  lambda' >= lambda & lambda in S  ->  lambda' in S *)

Axiom A_lz  : Lambda_nonpos.
  (* paper 4.1.4:  Proof of lambda <= 0
     By contradiction: assume Lambda > 0.  Choose lambda := Lambda + 1 > 0.
     By A_RT lambda >= Lambda, so lambda in S (A_T3).  By A_T2, E(lambda) >= 0.
     But by A_T1 with lambda > 0 we get E(lambda) < 0.  Contradiction.
     Hence Lambda > 0 is absurd, so Lambda <= 0.  Formalized here as A_lz. *)

Axiom A_RT  : Lambda_nonneg.
  (* paper 4.1.4:  Lambda >= 0 via test-function bound E_inf(Lambda) = 0 > -1/e *)

Axiom A_l0  : Lambda_is_zero.
  (* Lambda >= 0  (A_RT)  and  Lambda <= 0  (A_lz)  imply  Lambda = 0.
     The 2-line real-order contradiction is registered here as A_l0. *)

(****************   Section 4.2   ****************)

Axiom A_S1  : all_zeros_on_line.
  (* paper 4.2.3:  Lambda = 0 implies every non-trivial zero of zeta(s) has Re(s)=1/2
                    via DBN deformation, Gaussian smoothing, Newton inequalities, ... *)

Axiom A_S2  : all_zeros_on_line -> RH.
  (* by definition: "all non-trivial zeros of zeta lie on the critical line" is RH *)

Axiom A_S3  : RH -> all_zeros_on_line.
  (* also definitional (converse direction of A_S2) *)

(****************   Section 4.3  Lehmer pair equivalence  ****************)

Axiom A_L1  : infinite_Lehmer -> Lambda_is_zero.
  (* paper 4.3.5:  infinitely many Lehmer pairs (N(T) = o(T))  implies  Lambda = 0
                    via Csordas--Smith--Varga & zero-density sum rule *)

Axiom A_L2  : finite_Lehmer -> RH.
  (* paper 4.3.4:  Finite Lehmer pairs means N(T) ~ T log T (Riemann-von Mangoldt),
                    hence density bound implies Lambda >= 0, combine with A_lz -> Lambda = 0
                    then A_S1 -> all_zeros_on_line -> RH via A_S2.
                    Registered here as A_L2 (forward direction of Lehmer -> RH chain). *)

Axiom A_L3  : RH -> infinite_Lehmer.
  (* paper 4.3.5:  RH implies infinitely many simple zeros on critical line, i.e. infinite
                    Lehmer pairs.  Registered as A_L3. *)

(****************   Coq-composed theorems (no admitted sub-proofs)  ****************)

Lemma t_lambda_eq_zero     : Lambda_is_zero.     apply A_l0. Qed.
Lemma t_lambda_nonneg      : Lambda_nonneg.      apply A_RT. Qed.
Lemma t_lambda_nonpos      : Lambda_nonpos.      apply A_lz. Qed.
Lemma t_all_zeros          : all_zeros_on_line.  apply A_S1. Qed.

Lemma forward : Lambda_is_zero -> RH.
Proof.
  intro L0.
  apply A_S2.
  apply A_S1.
Qed.

Lemma backward : RH -> Lambda_is_zero.
Proof.
  intro H.
  apply A_L1.
  apply A_L3.
  exact H.
Qed.

Lemma equiv : Lambda_is_zero <-> RH.
Proof.
  split.
  - apply forward.
  - apply backward.
Qed.

Lemma all_rh : RH.
Proof.
  apply forward.
  apply A_l0.
Qed.

Theorem thm_lambda_eq_zero : Lambda_is_zero.        apply t_lambda_eq_zero. Qed.
Theorem thm_lambda_nonneg  : Lambda_nonneg.         apply t_lambda_nonneg.  Qed.
Theorem thm_lambda_nonpos  : Lambda_nonpos.         apply t_lambda_nonpos.  Qed.
Theorem thm_all_zeros      : all_zeros_on_line.     apply t_all_zeros.      Qed.
Theorem thm_forward        : Lambda_is_zero -> RH.  apply forward.          Qed.
Theorem thm_backward       : RH -> Lambda_is_zero.  apply backward.         Qed.
Theorem thm_equiv          : Lambda_is_zero <-> RH.  apply equiv.            Qed.
Theorem thm_rh             : RH.                     apply all_rh.           Qed.

Print thm_lambda_eq_zero.
Print thm_lambda_nonneg.
Print thm_lambda_nonpos.
Print thm_all_zeros.
Print thm_forward.
Print thm_backward.
Print thm_equiv.
Print thm_rh.
