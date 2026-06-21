From Stdlib Require Import Reals micromega.Lra.
Open Scope R_scope.
Goal forall x, x + 1 > x.
Proof.
  intro.
  assert (x + 1 - x > 0).
  ring_simplify. lra.
  lra.
Qed.
