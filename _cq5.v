From Coquelicot Require Import Coquelicot RInt Continuity Derive.
From Stdlib Require Import micromega.Lra.
Open Scope R_scope.

Lemma test_lra : forall x y, x < y -> x + 1 < y + 1.
Proof. intros. lra. Qed.

Lemma test_ring : forall a b, (a + b)^2 = a^2 + 2*a*b + b^2.
Proof. intros. ring. Qed.

Lemma test_sq_nonneg : forall x, x * x >= 0.
Proof. intro x.
  case (total_order_T x 0) as [|[|]].
  - nra.
  - nra.
  - nra.
Qed.

Lemma pythagoras_nonneg : forall a b, a^2 + b^2 = 0 -> a = 0 /\ b = 0.
Proof.
  intros a b H.
  have Ha : a^2 >= 0 by apply test_sq_nonneg.
  have Hb : b^2 >= 0 by apply test_sq_nonneg.
  nra.
Qed.

Print pythagoras_nonneg.
