From Stdlib Require Import Reals Lra Classical Classical_Prop.
Open Scope R_scope.

Lemma _c0': forall (y : R) (Heq : y = 0) (Hlt : y < 0), False.
Proof.
  intros y Heq Hlt.
  Print y.
  Show y.
Abort.