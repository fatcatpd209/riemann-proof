From Coquelicot Require Import Coquelicot RInt Continuity Derive.
Open Scope R_scope.

Lemma test_ring_only : forall a b, (a + b)^2 = a^2 + 2*a*b + b^2.
Proof. intros. ring. Qed.

Lemma test_sq_nonneg_real_ring : forall x, x^2 >= 0.
Proof. intro x.
  destruct (total_order_T x 0) as [G|[L|E]].
  - apply Rmult_le_pos; lra.
  - apply Rmult_le_pos; lra.
  - rewrite E. nra.
Qed.

Print test_sq_nonneg_real_ring.
