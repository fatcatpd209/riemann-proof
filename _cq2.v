From Coquelicot Require Import Coquelicot.
Open Scope R_scope.
Lemma test_0_plus_0 : 0 + 0 = 0. Proof. lra. Qed.
Lemma test_Rplus_comm : forall x y, x + y = y + x. Proof. intros. ring. Qed.
Lemma test_Rsq_nonneg : forall x, x * x >= 0. Proof. intros. nra. Qed.
Print test_Rsq_nonneg.
