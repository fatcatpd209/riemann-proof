From Stdlib Require Import Reals micromega.Lra.
Open Scope R_scope.

Check Rplus.
Check Rplus_comm.
Lemma test_real: forall a b, a + b = b + a.
Proof. intros; lra. Qed.

Print test_real.
