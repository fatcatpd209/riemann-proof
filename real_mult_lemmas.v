From Stdlib Require Import Reals Lra Classical Classical_Prop.
Open Scope R_scope.

Lemma Rmult_neg_pos_lt0 : forall a b : R, a < 0 -> 0 < b -> a * b < 0.
Proof.
  intros a b Ha Hb.
  assert (Hnegpos : -a > 0). lra.
  assert (Hprodpos : (-a) * b > 0).
    apply Rmult_lt_0_compat; assumption.
  assert (Hgoal : a * b < 0).
    rewrite <- (Ropp_mul_distr_l a b).
    rewrite Ropp_involutive in Hnegpos.
    lra.
  exact Hgoal.
Qed.

Lemma Rmult_pos_neg_lt0 : forall a b : R, 0 < a -> b < 0 -> a * b < 0.
Proof.
  intros a b Ha Hb.
  assert (Hnegpos : -b > 0). lra.
  assert (Hprodpos : a * (-b) > 0).
    apply Rmult_lt_0_compat; assumption.
  assert (Hgoal : a * b < 0).
    rewrite <- (Ropp_mul_distr_r a b).
    lra.
  exact Hgoal.
Qed.

Lemma Rmult_le_pos_le_pos : forall a b : R, 0 <= a -> 0 <= b -> 0 <= a * b.
Proof.
  intros a b Ha Hb.
  destruct (total_order_T a 0) as [[Ha0 | Heq] | Hgt].
  - exfalso. lra.
  - rewrite Heq. ring.
  - destruct (total_order_T b 0) as [[Hb0 | Heqb] | Hgtb].
    + exfalso. lra.
    + rewrite Heqb. ring.
    + apply Rmult_lt_0_compat; assumption.
Qed.

Lemma Rmult_le_pos_le_neg : forall a b : R, 0 <= a -> b <= 0 -> a * b <= 0.
Proof.
  intros a b Ha Hb.
  destruct (total_order_T a 0) as [[Ha0 | Heq] | Hgt].
  - exfalso. lra.
  - rewrite Heq. lra.
  - destruct (total_order_T b 0) as [[Hb0 | Heqb] | Hgtb].
    + lra.
    + rewrite Heqb. lra.
    + exfalso. lra.
Qed.

Lemma Rmult_le_neg_le_pos : forall a b : R, a <= 0 -> 0 <= b -> a * b <= 0.
Proof.
  intros a b Ha Hb.
  rewrite Rmult_comm. apply Rmult_le_pos_le_neg; lra.
Qed.

Lemma Rmult_le_neg_le_neg : forall a b : R, a <= 0 -> b <= 0 -> 0 <= a * b.
Proof.
  intros a b Ha Hb.
  rewrite <- (Ropp_mul_distr_l a b).
  rewrite <- (Ropp_mul_distr_r (-a) b).
  rewrite Ropp_involutive.
  assert (Hna : -a >= 0). lra.
  assert (Hnb : -b >= 0). lra.
  apply Rmult_le_pos_le_pos; assumption.
Qed.
