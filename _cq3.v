From Coquelicot Require Import Coquelicot RInt Continuity Derive.
From Stdlib Require Import micromega.Lra micromega.Nsatz.
Open Scope R_scope.

Lemma test_lra_after_coq : forall x y, x < y -> x + 1 < y + 1.
Proof. intros. lra. Qed.

Lemma test_Rsq_nonneg : forall x, x * x >= 0. Proof. intros. nra. Qed.

Lemma test_pow2_nonneg : forall x, x ^ 2 >= 0. Proof. intros. nra. Qed.

Lemma test_pythagoras_hint : forall a b, a^2 + b^2 = 0 -> a = 0 /\ b = 0.
Proof.
  intros a b H.
  assert (a^2 >= 0) by apply test_pow2_nonneg.
  assert (b^2 >= 0) by apply test_pow2_nonneg.
  nra.
Qed.

Print test_pythagoras_hint.
