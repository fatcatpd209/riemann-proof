From Stdlib Require Import Reals.
Open Scope R_scope.
Lemma t1 : forall l : R, l + 1 >= l.
Proof.
  intros l.
  pose proof (total_order_T (l + 1) l) as P.
  destruct P as [[Hlt|Heq]|Hgt].
  - exfalso.
    assert (contra : False) by admit. exact contra.
  - admit.
  - admit.
Qed.

Print t1.
