import javascript

from CallExpr call, FunctionExpr target
where target.getName() = "eval"
and exists(call.getArgument(0))
select call, "Possible eval-based backdoor"
