From Stdlib Require Import Reals Lra Classical Classical_Prop.
Open Scope R_scope.

Lemma Rnegneg_pos : forall x y : R, x <= 0 -> y <= 0 -> 0 <= x * y.
Proof.
  intros x y Hx Hy.
  pose proof (total_order_T x 0) as Htx.
  pose proof (total_order_T y 0) as Hty.
  destruct Htx as [[Hxlt | Hxeq] | Hxgt].
    destruct Hty as [[Hylt | Hyeq] | Hygt].
      assert (Hnxgt : 0 < -x). lra.
      assert (Hnygt : 0 < -y). lra.
      assert (Hprodpos : 0 < (-x) * (-y)). apply Rmult_lt_0_compat; assumption.
      assert (Heq : (-x) * (-y) = x * y). ring.
      cut (0 <= (-x) * (-y)).
        intros H. rewrite Heq. exact H.
        lra.
    rewrite Hyeq. lra.
    exfalso. lra.
  rewrite Hxeq. lra.
  exfalso. lra.
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
  pose proof (total_order_T y 0) as Hty.
  destruct Hty as [[Hylt | Hyeq] | Hygt].
    assert (Hnygt : 0 < -y). lra.
    assert (H1 : 0 <= x * (-y)). apply Rmult_le_pos; lra.
    assert (H2 : x * (-y) = - (x * y)). ring.
    cut (0 <= x * (-y)). intros H. rewrite H2 in H. lra.
    exact H1.
  rewrite Hyeq. lra.
  exfalso. lra.
Qed.

Lemma Rnegposneg_neg : forall x y : R, x <= 0 -> 0 <= y -> x * y <= 0.
Proof.
  intros x y Hx Hy. rewrite Rmult_comm. apply Rposposneg_neg; lra.
Qed.
