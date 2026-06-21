From Stdlib Require Import Reals.
From Stdlib.micromega Require Import Lra.
Lemma testR : forall l : R, l + 1 >= l.
Proof. intro l. cbv. lra. Qed.
Print testR.
