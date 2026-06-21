Require Import Reals Lra Classical Classical_Prop.
Open Scope R_scope.
Lemma foo : forall (a b : R), a < 0 -> 0 < b -> a * b < 0.
Proof.
  intros a b Ha Hb.
  assert (H : a * b = -((-a) * b)). ring.
  rewrite H.
  assert (H2 : -a > 0). lra.
  assert (H3 : (-a) * b > 0).
    apply Rmult_lt_0_compat. exact H2. exact Hb.
  lra.
Qed.
Print foo.
