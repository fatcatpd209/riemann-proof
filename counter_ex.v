From Stdlib Require Import Reals Lra.
Require Import base_library main_proof.

Open Scope R_scope.

Lemma model_embed_spectral_sign_placeholder :
  forall (Hspace_t : Type) (ip_t : Hspace_t -> Hspace_t -> R) (ps_t : Hspace_t -> Hspace_t)
         (Hsd : forall x, 0 <= ip_t x (ps_t x)),
  (forall lam : R,
    (exists x, ip_t x x > 0 /\ ip_t (ps_t x) x = lam * ip_t x x) -> 0 <= lam) ->
  (forall lam : R, (exists x, ip_t x x > 0 /\ ip_t (ps_t x) x = lam * ip_t x x) -> 0 <= lam).
Proof.
  intros Hsp ip ps Hpsd H1 lam H2. apply H1. exact H2.
Qed.

Section CounterExample_Bridge.

Definition R2_space : Type := prod R R.
Definition R2_inner_product (x y : R2_space) : R :=
  match x with
  | (x1, x2) =>
    match y with
    | (y1, y2) => x1 * y1 + x2 * y2
    end
  end.
Definition R2_ps_op_neg (x : R2_space) : R2_space :=
  match x with
  | (x1, x2) => (- x1, - x2)
  end.

Lemma R2_inner_product_selfadj_ok :
  forall x y, R2_inner_product (R2_ps_op_neg x) y = R2_inner_product x (R2_ps_op_neg y).
Proof.
  intros [x1 x2] [y1 y2].
  unfold R2_inner_product, R2_ps_op_neg.
  cbn.
  ring.
Qed.

Lemma R2_psd_fails_neg :
  exists x, 0 > R2_inner_product x (R2_ps_op_neg x).
Proof.
  exists (1, 0).
  unfold R2_inner_product, R2_ps_op_neg.
  cbn. lra.
Qed.

End CounterExample_Bridge.

Section DAG_Check.

Lemma DAG_layer_1_logic :
  forall P Q : Prop, (P -> Q) -> (~ Q -> ~ P).
Proof. apply contrapositive. Qed.

Lemma DAG_layer_2_real_arith :
  forall x y : R, x <= 0 -> y <= 0 -> 0 <= x * y.
Proof. apply Rnegneg_pos. Qed.

Lemma DAG_layer_3_spectral_axiom :
  forall (H_space_T : Type)
         (inner_product_T : H_space_T -> H_space_T -> R)
         (ps_op_T : H_space_T -> H_space_T)
         (Hselfadj : forall x y, inner_product_T (ps_op_T x) y = inner_product_T x (ps_op_T y))
         (Hpsd : forall x, 0 <= inner_product_T x (ps_op_T x)),
    forall lam, (exists x, inner_product_T x x > 0 /\
      inner_product_T (ps_op_T x) x = lam * inner_product_T x x) -> 0 <= lam.
Proof.
  intros H_space inner ps selfadj psd.
  apply (L416_POSITIVE_SPECTRAL H_space inner ps selfadj psd).
Qed.

End DAG_Check.
