Require Import Reals Lra Classical Psatz List Arith.
From Coquelicot Require Import Rbar Derive.

Parameter Derive_at : (Rbar -> Rbar) -> Rbar -> Rbar.

Parameter Derive_id :
  forall (x : Rbar), Derive_at (fun u : Rbar => u) x = Finite 1.

Parameter Derive_const_zero :
  forall (c : Rbar) (x : Rbar), Derive_at (fun _ : Rbar => c) x = Finite 0.

Parameter Derive_scalar_mult :
  forall (c : Rbar) (f : Rbar -> Rbar) (x : Rbar),
  Derive_at (fun u : Rbar => Rbar_mult c (f u)) x = Rbar_mult c (Derive_at f x).

Parameter Derive_sum :
  forall (f : Rbar -> Rbar) (g : Rbar -> Rbar) (x : Rbar),
  Derive_at (fun u : Rbar => Rbar_plus (f u) (g u)) x = Rbar_plus (Derive_at f x) (Derive_at g x).

Parameter gaussian_integral_proportionality : forall sigma mu : R, sigma > 0 -> Prop.
Parameter h_lambda_t_cosine_transform : forall lambda t : R, Prop.
Parameter integrate_by_parts_sketch : forall (f : R -> R) (g : R -> R) (a b : R), Prop.
Parameter cauchy_schwarz_rint : forall (f : R -> R) (g : R -> R) (a b : R), Prop.
Parameter derivative_chain_rule_sketch : forall (f : Rbar -> Rbar) (g : Rbar -> Rbar) (x : Rbar), Prop.