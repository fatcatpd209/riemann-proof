From Stdlib Require Import Reals Lra.
Open Scope R_scope.

Lemma real_contrad_le_ge : forall x : R, x <= 0 -> 0 <= x -> x = 0.
Proof.
  intros x Hle Hge.
  assert (Hdec : x < 0 \/ ~ (x < 0)). { destruct (Rlt_le_dec x 0) as [Hlt | Hge0]. left. exact Hlt. right. lra. }
  destruct Hdec as [Hlt | Hnlt].
  - exfalso. lra.
  - assert (Hxeq : x = 0). lra. exact Hxeq.
Qed.

Lemma real_contrad_lt_ge : forall x : R, x < 0 -> 0 <= x -> False.
Proof.
  intros x Hlt Hge.
  assert (Hle : x <= 0). lra.
  assert (Hxeq : x = 0). { apply real_contrad_le_ge; assumption. }
  assert (H0lt0 : 0 < 0).
    rewrite Hxeq in Hlt.
    assumption.
  assert (Hirr : ~ (0 < 0)). { apply Rlt_irrefl. }
  exact (Hirr H0lt0).
Qed.

Lemma real_contrad_le_gt : forall x : R, x <= 0 -> 0 < x -> False.
Proof.
  intros x Hle Hgt.
  assert (Hge : 0 <= x). lra.
  assert (Hxeq : x = 0). { apply real_contrad_le_ge; assumption. }
  assert (H0gt0 : 0 < 0).
    rewrite Hxeq in Hgt.
    assumption.
  assert (Hirr : ~ (0 < 0)). { apply Rlt_irrefl. }
  exact (Hirr H0gt0).
Qed.

Lemma real_contrad_lt_gt : forall x : R, x < 0 -> 0 < x -> False.
Proof.
  intros x Hlt Hgt.
  assert (Hle : x <= 0). lra.
  apply real_contrad_le_gt with (x := x); assumption.
Qed.

Lemma real_contrad_pos_neg : forall x : R, 0 < x -> x < 0 -> False.
Proof.
  intros x Hpos Hneg.
  apply real_contrad_lt_gt with (x := x); assumption.
Qed.

Lemma real_le_ge_eq0 : forall x : R, x <= 0 -> 0 <= x -> x = 0.
Proof.
  exact real_contrad_le_ge.
Qed.

Lemma contrapositive_PQ : forall P Q : Prop, (P -> Q) -> (~Q -> ~P).
Proof.
  intros P Q H Hnq.
  intros Hp.
  apply Hnq. apply H. exact Hp.
Qed.

Lemma modus_tollens : forall P Q : Prop, (P -> Q) -> ~Q -> ~P.
Proof.
  exact contrapositive_PQ.
Qed.

Lemma and_cancel_l : forall P Q : Prop, P /\ Q -> P.
Proof. intros P Q H. destruct H. exact H. Qed.

Lemma and_cancel_r : forall P Q : Prop, P /\ Q -> Q.
Proof. intros P Q H. destruct H. exact H0. Qed.

Lemma or_introl_map : forall P Q R : Prop, (P -> R) -> (P \/ Q) -> (R \/ Q).
Proof. intros P Q R H [Hp | Hq]. left. apply H. exact Hp. right. exact Hq. Qed.

Lemma or_intror_map : forall P Q R : Prop, (Q -> R) -> (P \/ Q) -> (P \/ R).
Proof. intros P Q R H [Hp | Hq]. left. exact Hp. right. apply H. exact Hq. Qed.
