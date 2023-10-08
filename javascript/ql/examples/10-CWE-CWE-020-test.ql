import javascript

from CallExpr call, FunctionExpr target
where target.getName() = "eval"
and exists(call.getArgument(0))
select call,call.getFile().getAbsolutePath()+"$$"+call.getFile().getLocation().getStartLine(), "Possible eval-based backdoor"
