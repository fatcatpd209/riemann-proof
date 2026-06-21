From Coquelicot Require Import Coquelicot RInt Continuity Derive.
Open Scope R_scope.

Lemma sq : forall x, x * x >= 0.
Proof. intro x.
  destruct (total_order_T x 0) as [G|[L|E]].
  - apply Rmult_le_pos; lra.
  - apply Rmult_le_pos; lra.
  - rewrite E. nra.
Qed.

Lemma pyth_nonneg : forall a b, a*a + b*b = 0 -> a = 0 /\ b = 0.
Proof. intros a b H.
  have Ha : a*a >= 0 by apply sq.
  have Hb : b*b >= 0 by apply sq.
  nra.
Qed.

Open Scope Rpow.
Lemma sq2 : forall x : R, x ^ 2 >= 0.
Proof. intro x.
  destruct (total_order_T x 0) as [G|[L|E]].
  - apply Rmult_le_pos; lra.
  - apply Rmult_le_pos; lra.
  - rewrite E. nra.
Qed.

Print pyth_nonneg.
Print sq2.
