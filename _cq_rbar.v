From Coquelicot Require Import Coquelicot RInt Continuity Derive ElemFct Lub Rbar.
Open Scope Rbar_scope.

Locate "+".
Locate "*".
Locate "<=".
Locate "exp".
Locate "cos".
Locate "sin".

Print Rbar_scope.

Parameter my_sq : forall x, x * x >= 0.
Check my_sq.
