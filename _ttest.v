From Stdlib Require Import Reals Lra.
Open Scope R_scope.

Lemma tnegneg : forall x y, x <= 0 -> y <= 0 -> 0 <= x * y.
Proof.
  intros x y Hx Hy.
  assert (Hna : -x >= 0). lra.
  assert (Hnb : -y >= 0). lra.
  assert (Hpos : 0 <= (-x) * (-y)). apply Rmult_le_pos; assumption.
  assert (Hring : (-x) * (-y) = x * y).
    apply Ropp_mul_distr_l.
  rewrite Hring in Hpos. exact Hpos.
Qed.
