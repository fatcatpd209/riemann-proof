From Stdlib Require Import Reals Lra Classical Classical_Prop.
Open Scope R_scope.

Lemma Rnegpos_lt0 : forall x y : R, x < 0 -> 0 < y -> x * y < 0.
Proof.
  intros x y Hx Hy.
  assert (Hx' : 0 < -x). lra.
  assert (H1 : 0 < (-x) * y). apply Rmult_lt_0_compat; assumption.
  assert (H2 : (-x) * y = - (x * y)). ring.
  assert (H3 : 0 < - (x * y)).
    assert (H4 : (-x) * y = - (x * y)). ring.
    rewrite H4 in H1. exact H1.
  lra.
Qed.

Lemma Rposneg_lt0 : forall x y : R, 0 < x -> y < 0 -> x * y < 0.
Proof.
  intros x y Hx Hy.
  assert (Hy' : 0 < -y). lra.
  assert (H1 : 0 < x * (-y)). apply Rmult_lt_0_compat; assumption.
  assert (H2 : x * (-y) = - (x * y)). ring.
  assert (H3 : 0 < - (x * y)).
    assert (H4 : x * (-y) = - (x * y)). ring.
    rewrite H4 in H1. exact H1.
  lra.
Qed.

Lemma Rpospos_pos : forall x y : R, 0 <= x -> 0 <= y -> 0 <= x * y.
Proof.
  intros x y Hx Hy. apply Rmult_le_pos; assumption.
Qed.

Lemma Rposposneg_neg : forall x y : R, 0 <= x -> y <= 0 -> x * y <= 0.
Proof.
  intros x y Hx Hy.
  assert (Hneg : -y >= 0). lra.
  assert (Hpos : 0 <= x * (-y)). apply Rmult_le_pos; assumption.
  assert (Hring : x * (-y) = - (x * y)). ring.
  assert (Hneggoal : 0 <= - (x * y)).
    assert (H4 : x * (-y) = - (x * y)). ring.
    rewrite H4 in Hpos. exact Hpos.
  lra.
Qed.

Lemma Rnegposneg_neg : forall x y : R, x <= 0 -> 0 <= y -> x * y <= 0.
Proof.
  intros x y Hx Hy. rewrite Rmult_comm. apply Rposposneg_neg; lra.
Qed.

Lemma Rnegneg_pos : forall x y : R, x <= 0 -> y <= 0 -> 0 <= x * y.
Proof.
  intros x y Hx Hy.
  assert (Hna : -x >= 0). lra.
  assert (Hnb : -y >= 0). lra.
  assert (Hpos : 0 <= (-x) * (-y)). apply Rmult_le_pos; assumption.
  assert (Hring1 : (-x) * (-y) = - (x * (-y))). ring.
  assert (Hring2 : x * (-y) = - (x * y)). ring.
  assert (Htrans : (-x) * (-y) = x * y).
    ring.
  assert (Hfinal : 0 <= x * y).
    rewrite <- Htrans. exact Hpos.
  exact Hfinal.
Qed.
