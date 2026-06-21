From Coquelicot Require Import Coquelicot RInt Continuity Derive ElemFct Lub.
From Stdlib Require Import micromega.Lra.
Open Scope R_scope.

Lemma sq_simple : forall x, x * x >= 0.
Proof. intro x.
  destruct (total_order_T x 0) as [G|[L|E]].
  - apply Rmult_le_pos; lra.
  - apply Rmult_le_pos; lra.
  - rewrite E. nra.
Qed.

Lemma pyth_nonneg : forall a b, a*a + b*b = 0 -> a = 0 /\ b = 0.
Proof. intros a b H.
  have Ha : a*a >= 0 by apply sq_simple.
  have Hb : b*b >= 0 by apply sq_simple.
  nra.
Qed.

Lemma positive_implies_sq_pos : forall x, x > 0 -> x * x > 0.
Proof.
  intros x H.
  have H1 : x * x >= 0 by apply sq_simple.
  have H2 : x * x <> 0.
  - intro H3.
    have H4 : x * x = 0 by exact H3.
    have H5 : x = 0 by nra.
    exfalso. lra.
  have H : x * x > 0. nra. exact H.
Qed.

Lemma integral_ineq_hint :
  forall f g (a b : R),
  (forall x, a <= x -> x <= b -> f x <= g x) ->
  RInt f a b <= RInt g a b.
Proof.
  admit.
Admitted.

Lemma cauchy_schwarz_factoring :
  forall a b c d : R,
  (a*c + b*d)^2 <= (a*a + b*b) * (c*c + d*d).
Proof.
  intros. nra.
Qed.

Print pyth_nonneg.
Print positive_implies_sq_pos.
Print cauchy_schwarz_factoring.
