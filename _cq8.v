From Coquelicot Require Import Coquelicot RInt Continuity Derive Rpow_def.
From Stdlib Require Import micromega.Lra Rorder.
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

Open Scope powR_scope.
Lemma sq_powR : forall x : R, x ^ 2 >= 0.
Proof. intro x.
  destruct (total_order_T x 0) as [G|[L|E]].
  - apply Rmult_le_pos; lra.
  - apply Rmult_le_pos; lra.
  - rewrite E. nra.
Qed.

Print sq_powR.
Print pyth_nonneg.
