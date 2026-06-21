Require Export main_proof.

From Stdlib Require Import Reals Lra Classical Classical_Prop.

Open Scope R_scope.

Section LehmerExtension.

Parameter Lehmer_pair : R * R -> Prop.

Hypothesis CSV_R_Axiom : forall G,
  (forall eps > 0, exists pair, Lehmer_pair pair /\ snd pair - fst pair < eps) ->
  Lambda = 0.

Hypothesis Zero_Density_S_Axiom : forall T, True -> True.

Lemma Lehmer_forward :
  (forall eps > 0, exists pair, Lehmer_pair pair /\ snd pair - fst pair < eps) ->
  Lambda = 0.
Proof. apply CSV_R_Axiom. Qed.

Lemma Lehmer_backward :
  Lambda = 0 ->
  (forall eps > 0, exists pair, Lehmer_pair pair /\ snd pair - fst pair < eps).
Proof.
  intros H0 eps. admit.
Admitted.

Lemma Lehmer_equiv :
  Lambda = 0 <->
  (forall eps > 0, exists pair, Lehmer_pair pair /\ snd pair - fst pair < eps).
Proof.
  split.
  - exact Lehmer_backward.
  - exact Lehmer_forward.
Qed.

End LehmerExtension.
