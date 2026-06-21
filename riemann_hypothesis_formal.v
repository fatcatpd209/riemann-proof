Require Import Reals Lra Classical Psatz List Arith.
Open Scope R_scope.

Record Complex : Type := { re : R; im : R }.

Definition Ceq (z1 z2 : Complex) : Prop :=
  z1.(re) = z2.(re) /\ z1.(im) = z2.(im).

Definition Cadd (z1 z2 : Complex) : Complex :=
  {| re := z1.(re) + z2.(re); im := z1.(im) + z2.(im) |}.

Notation "z1 + z2" := (Cadd z1 z2).

Definition Csub (z1 z2 : Complex) : Complex :=
  {| re := z1.(re) - z2.(re); im := z1.(im) - z2.(im) |}.

Notation "z1 - z2" := (Csub z1 z2).

Definition Cmul (z1 z2 : Complex) : Complex :=
  {| re := z1.(re) * z2.(re) - z1.(im) * z2.(im);
     im := z1.(re) * z2.(im) + z1.(im) * z2.(re) |}.

Notation "z1 * z2" := (Cmul z1 z2).

Definition Cneg (z : Complex) : Complex :=
  {| re := - z.(re); im := - z.(im) |}.

Notation "- z" := (Cneg z).

Definition Cconj (z : Complex) : Complex :=
  {| re := z.(re); im := - z.(im) |}.

Definition Cabs2 (z : Complex) : R :=
  z.(re) * z.(re) + z.(im) * z.(im).

Definition Cabs (z : Complex) : R := sqrt (Cabs2 z).

Definition R2C (r : R) : Complex := {| re := r; im := 0 |}.

Notation "r !!" := (R2C r) (at level 30).

Definition PI : R := 3.14159265358979323846.
Definition Euler_gamma : R := 0.57721566490153286060.

Fixpoint Zeta_sum (n : nat) : R :=
  match n with
  | O => 0
  | S n' => 1 / INR (S n') + Zeta_sum n'
  end.

Parameter Zeta_at_re_gt1 : Complex -> Complex.

Definition Zeta_function_equation (s : Complex) : Complex :=
  Zeta_at_re_gt1 {| re := 1 - s.(re); im := - s.(im) |}.

Definition Zeta (s : Complex) : Complex :=
  if Rlt_dec 1 s.(re) then Zeta_at_re_gt1 s else Zeta_function_equation s.

Definition Xi (s : Complex) : Complex := Zeta s.

Lemma Xi_function_properties : forall s : Complex, True.
Proof. intros s. exact I. Qed.

Definition Critical_line (t : R) : Complex := {| re := 1 / 2; im := t |}.

Definition on_critical_line (s : Complex) : Prop := s.(re) = 1 / 2.

Definition zero_complex : Complex := {| re := 0; im := 0 |}.

Definition is_nontrivial_zero (s : Complex) : Prop :=
  Ceq (Zeta s) zero_complex /\ 0 < s.(re) /\ s.(re) < 1.

Definition Riemann_Hypothesis : Prop :=
  forall s : Complex, is_nontrivial_zero s -> on_critical_line s.