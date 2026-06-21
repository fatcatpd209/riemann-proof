From Stdlib Require Import Reals Lra Classical Classical_Prop.
Open Scope R_scope.

Lemma Rnegneg_pos : forall x y : R, x <= 0 -> y <= 0 -> 0 <= x * y.
Proof.
  intros x y Hx Hy.
  pose proof (total_order_T x 0) as Htx.
  pose proof (total_order_T y 0) as Hty.
  destruct Htx as [[Hxlt | Hxeq] | Hxgt].
  - destruct Hty as [[Hylt | Hyeq] | Hygt].
    + assert (Hnxgt : 0 < -x). lra.
      assert (Hnygt : 0 < -y). lra.
      assert (Hprod : 0 < (-x) * (-y)). apply Rmult_lt_0_compat; assumption.
      assert (Hmain : 0 <= x * y). lra.
      exact Hmain.
    + lra.
    + lra.
  - destruct Hty as [[Hylt | Hyeq] | Hygt].
    + lra.
    + rewrite Hxeq. lra.
    + lra.
  - destruct Hty as [[Hylt | Hyeq] | Hygt].
    + lra.
    + lra.
    + lra.
Qed.
