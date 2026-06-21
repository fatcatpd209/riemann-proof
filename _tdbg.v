From Stdlib Require Import Reals Lra.
Open Scope R_scope.

Lemma foo2 : forall a b : R, 0 <= a -> 0 <= b -> 0 <= a * b.
Proof.
  intros a b Ha Hb. lra.
Qed.

Lemma foo3 : forall a b : R, 0 < a -> 0 < b -> 0 < a * b.
Proof.
  intros a b Ha Hb. apply Rmult_lt_0_compat; assumption.
Qed.

Lemma foo4 : forall a b : R, a <= 0 -> 0 <= b -> a * b <= 0.
Proof.
  intros a b Ha Hb. lra.
Qed.

Lemma foo5 : forall a b : R, a < 0 -> 0 < b -> a * b < 0.
Proof.
  intros a b Ha Hb.
  assert (H1 : -a > 0). lra.
  assert (H2 : - (a * b) > 0).
    cut ((-a) * b > 0).
    - intros H. lra.
    - apply Rmult_lt_0_compat; assumption.
  lra.
Qed.
