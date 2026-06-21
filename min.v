From Stdlib Require Import Reals Lra Classical Classical_Prop.
Open Scope R_scope.

Lemma real_contrad_lt_ge : forall (a b : R), a < b -> a = b -> False.
Proof.
  intros a b Hlt Heq.
  induction Hlt.
  + assert (Ht : a = a + pos). ring.
    rewrite <- Heq in Hlt.
    assert (Hc : False).
      assert (Hcontra : (a + pos) <= a). lra.
      assert (Hcontra2 : a < a). lra.
      exfalso. apply Rlt_irrefl with (x := a). lra.
    exact Hc.
  + rewrite Hlt.
    induction Heq.
    * exfalso. apply Rlt_irrefl with (x := b0). lra.
    * exfalso. apply Rlt_irrefl with (x := b0). lra.
Qed.