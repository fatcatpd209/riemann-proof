From Stdlib Require Import Reals Lra Classical Classical_Prop.
Open Scope R_scope.

Lemma Rnegneg_pos : forall x y : R, x <= 0 -> y <= 0 -> 0 <= x * y.
Proof.
  intros x y Hx Hy.
  destruct (classical (x = 0)) as [Hxeq | Hxne].
    rewrite Hxeq. lra.
  destruct (classical (y = 0)) as [Hyeq | Hyne].
    rewrite Hyeq. lra.
  assert (Hxlt : x < 0). lra.
  assert (Hylt : y < 0). lra.
  assert (Hnxgt : 0 < -x). lra.
  assert (Hnygt : 0 < -y). lra.
  assert (Hprodpos : 0 < (-x) * (-y)). apply Rmult_lt_0_compat; assumption.
  assert (Halt : (-x) * (-y) >= 0). lra.
  assert (Heq : (-x) * (-y) = x * y). ring.
  rewrite Heq in Halt. exact Halt.
Qed.

Lemma Rnegpos_lt0 : forall x y : R, x < 0 -> 0 < y -> x * y < 0.
Proof.
  intros x y Hx Hy.
  assert (Hnxgt : 0 < -x). lra.
  assert (H1 : 0 < (-x) * y). apply Rmult_lt_0_compat; assumption.
  assert (H2 : (-x) * y = - (x * y)). ring.
  rewrite H2 in H1. lra.
Qed.

Lemma Rposneg_lt0 : forall x y : R, 0 < x -> y < 0 -> x * y < 0.
Proof.
  intros x y Hx Hy.
  assert (Hnygt : 0 < -y). lra.
  assert (H1 : 0 < x * (-y)). apply Rmult_lt_0_compat; assumption.
  assert (H2 : x * (-y) = - (x * y)). ring.
  rewrite H2 in H1. lra.
Qed.

Lemma Rpospos_pos : forall x y : R, 0 <= x -> 0 <= y -> 0 <= x * y.
Proof.
  intros x y Hx Hy. apply Rmult_le_pos; assumption.
Qed.

Lemma Rposposneg_neg : forall x y : R, 0 <= x -> y <= 0 -> x * y <= 0.
Proof.
  intros x y Hx Hy.
  destruct (classical (y = 0)) as [Hyeq | Hyne].
    rewrite Hyeq. lra.
  assert (Hylt : y < 0). lra.
  assert (Hnygt : 0 < -y). lra.
  assert (H1 : 0 <= x * (-y)). apply Rmult_le_pos; lra.
  assert (H2 : x * (-y) = - (x * y)). ring.
  rewrite H2 in H1. lra.
Qed.

Lemma Rnegposneg_neg : forall x y : R, x <= 0 -> 0 <= y -> x * y <= 0.
Proof.
  intros x y Hx Hy. rewrite Rmult_comm. apply Rposposneg_neg; lra.
Qed.
