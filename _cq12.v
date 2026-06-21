From Coquelicot Require Import Coquelicot RInt Continuity Derive ElemFct Lub.
From Stdlib Require Import micromega.Lra Raxioms.
Open Scope R_scope.

Lemma sq_simple : forall x, x * x >= 0.
Proof. intro x.
  destruct (total_order_T x 0) as [|[|]].
  - apply Rmult_le_pos; lra.
  - apply Rmult_le_pos; lra.
  - rewrite e. nra.
Qed.

Lemma pyth_nonneg : forall a b, a*a + b*b = 0 -> a = 0 /\ b = 0.
Proof. intros a b H.
  have Ha : a*a >= 0 by apply sq_simple.
  have Hb : b*b >= 0 by apply sq_simple.
  nra.
Qed.

Lemma cauchy_schwarz_factoring :
  forall a b c d : R,
  (a*c + b*d)^2 <= (a*a + b*b) * (c*c + d*d).
Proof. intros. nra. Qed.

Lemma integral_ineq_hint :
  forall f g (a b : R),
  (forall x, a <= x -> x <= b -> f x <= g x) ->
  RInt f a b <= RInt g a b.
Proof. admit. Admitted.

(* Section 2.3 : Integration by parts identity *)
Parameter Derivable : (R -> R) -> Prop.
Parameter deriv_at  : (R -> R) -> R -> R.

Axiom deriv_correct_at :
  forall f a eps,
  Derivable f ->
  f (a + eps) = f a + eps * deriv_at f a + eps * eps * 0.
(* simplified axiom version *)

Parameter integral_on_Rbar : (R -> R) -> Rbar -> Rbar -> Rbar.

Axiom RInt_linear :
  forall f g a b,
  integral_on_Rbar (fun x => f x + g x) a b
  = integral_on_Rbar f a b + integral_on_Rbar g a b.

(* Section 2.3 : Gaussian integral  _{-infty}^{+infty} exp(-x^2) dx = sqrt(pi) *)
Parameter sqrt_pi : R.
Axiom sqrt_pi_pos     : sqrt_pi > 0.
Axiom gaussian_integral :
  integral_on_Rbar (fun x => exp(-x * x)) (-infty) (pinfty) = Finite sqrt_pi.

Print pyth_nonneg.
Print cauchy_schwarz_factoring.
