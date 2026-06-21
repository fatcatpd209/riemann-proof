From Stdlib Require Import Reals Lra Classical Classical_Prop.
Require Import base_library.

Open Scope R_scope.

Section MainProof.

Parameter Lambda : R.
Parameter RH : Prop.

Hypothesis H_Lambda_nonneg : 0 <= Lambda.
Hypothesis H_RH_eq : Lambda = 0 <-> RH.

Lemma T451_RH_forward : Lambda = 0 -> RH.
Proof.
  intros H. apply H_RH_eq. exact H.
Qed.

Lemma T451_RH_backward : RH -> Lambda = 0.
Proof.
  intros H. apply H_RH_eq. exact H.
Qed.

Lemma T451_RH_equiv : Lambda = 0 <-> RH.
Proof.
  split.
  - apply T451_RH_forward.
  - apply T451_RH_backward.
Qed.

Lemma L417_main_chain :
  (Lambda = 0 -> RH) -> (~ RH -> Lambda <> 0).
Proof.
  apply contrapositive.
Qed.

End MainProof.
