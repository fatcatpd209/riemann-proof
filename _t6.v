From Stdlib Require Import Reals Lra Classical Classical_Prop.
Open Scope R_scope.

Lemma sign_flip : forall x y : R, (-x) * (-y) = x * y.
Proof.
  intros.
  ring.
Qed.

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
      assert (Heq : (-x) * (-y) = x * y). apply sign_flip.
      assert (Hmain : 0 <= (-x) * (-y)). lra.
      assert (Hfinal : 0 <= x * y). rewrite <- Heq. exact Hmain.
      exact Hfinal.
    rewrite Hyeq. lra.
    exfalso. lra.
  rewrite Hxeq. lra.
  exfalso. lra.
Qed.
