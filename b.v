From Stdlib Require Import Reals.
From Stdlib.micromega Require Import Lra.
Open Scope R_scope.
Parameter S_sub  : R -> Prop.
Parameter Lambda : R.
Parameter E_fun  : R -> R.
Axiom A_T1 : forall lam, lam > 0 -> E_fun lam < 0.
Axiom A_T2 : forall lam, S_sub lam -> E_fun lam >= 0.
Axiom A_T3 : forall lam, lam >= Lambda -> S_sub lam.
Axiom A_RT : Lambda >= 0.
Lemma test_arith : forall l : R, l + 1 >= l.
Proof.
  intro l.
  pose proof (total_order_T (l + 1) l) as P.
  destruct P as [[Hlt|Heq]|Hgt].
  - exfalso. lra.
  - lra.
  - lra.
Qed.
