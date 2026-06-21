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

Lemma basic_test : Lambda > 0 -> False.
Proof.
  intro Hpos.
  lra.
Qed.

Print basic_test.
