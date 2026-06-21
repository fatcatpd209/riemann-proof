From Coquelicot Require Import Coquelicot RInt Continuity Derive ElemFct Lub.
From Stdlib Require Import micromega.Lra Raxioms.
Open Scope R_scope.

Lemma sq_simple : forall x, x * x >= 0.
Proof. intro x.
  destruct (total_order_T x 0) as [|[|]].
  - apply Rmult_le_pos; lra.
  - apply Rmult_le_pos; lra.
  - rewrite e. nra.
Qed.

Lemma pyth_nonneg : forall a b, a*a + b*b = 0 -> a = 0 /\ b = 0.
Proof. intros a b H.
  have Ha : a*a >= 0 by apply sq_simple.
  have Hb : b*b >= 0 by apply sq_simple.
  nra.
Qed.

Lemma cauchy_schwarz_factoring :
  forall a b c d : R,
  (a*c + b*d)^2 <= (a*a + b*b) * (c*c + d*d).
Proof. intros. nra. Qed.

Lemma integral_ineq_hint :
  forall f g (a b : R),
  (forall x, a <= x -> x <= b -> f x <= g x) ->
  RInt f a b <= RInt g a b.
Proof. admit. Admitted.

Lemma pos_gt_sq_lt : forall k, k > 0 -> forall x, x <= k * x * x.
Proof. intros k H x. nra. Qed.

Lemma linear_preserves_pos :
  forall a b x, a > 0 -> b >= 0 -> x >= 0 -> a * x + b >= 0.
Proof. intros a b x Ha Hb Hx. nra. Qed.

Print pyth_nonneg.
Print cauchy_schwarz_factoring.
