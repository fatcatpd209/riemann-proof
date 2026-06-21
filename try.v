From Stdlib.micromega Require Import Lra.
Lemma testR : forall l : R, l + 1 >= l.
Proof.
  intro l. lra.
Qed.
