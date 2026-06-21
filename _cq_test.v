From Coquelicot Require Import Reals.
Open Scope R_scope.
Goal forall a b : R, a < b -> a + 1 < b + 1.
Proof. intros. lra. Qed.
Print "hello".
