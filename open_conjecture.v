Require Import main_proof.

From Stdlib Require Import Reals Lra Classical Classical_Prop.

Open Scope R_scope.

Section PolyaConj.

Parameter Phi : R -> R.
Parameter completely_monotone : (R -> R) -> Prop.

Conjecture Polya_equiv : forall lam,
  S_set lam <-> completely_monotone (fun u : R => Phi (lam * u * u)).

Conjecture Csordas_Smith_asym :
  forall M, exists lam, lam < -M.

End PolyaConj.
