From Coquelicot Require Import Coquelicot RInt Continuity Derive ElemFct Lub.

(* --- 基础实数公理（从 Coquelicot 继承的 Stdlib Reals） --- *)
Parameter R_plus : Set.
Parameter R_zero : R_plus.
Parameter R_one  : R_plus.

(* 我们直接使用 Coquelicot 的 R 类型（它是 Rbar 下的 Finite），所以
   用 Coquelicot.scope_R 或类似方式打开 scope *)

Locate Scope.
About R_scope.

(* 换个做法：直接不用 Open Scope R_scope *)
