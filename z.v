From Stdlib Require Import ZArith.
From Stdlib.micromega Require Import Zlia.
Lemma testZ : forall l : Z, l + 1 >= l.
Proof. intro l. lia. Qed.
Print testZ.
