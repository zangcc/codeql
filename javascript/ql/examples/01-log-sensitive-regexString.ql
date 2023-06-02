import javascript

from CallExpr call,string tempStr,string loc
where
  // 调用了 error(), INFO()函数
  call.getCalleeName().regexpMatch("(?i)(error|log|info|trace|debug)")  and
  // 循环判断每个参数是否包含敏感词
  exists(int i | i in [0 .. call.getNumArgument() - 1] |
    call.getArgument(i).toString().regexpMatch("(?i).*(key|password|secret|vault|param|arn|text|email|content|token|mail|ldap|response|request).*") and 
    not call.getArgument(i) instanceof StringLiteral and 
    tempStr = call.getArgument(i).toString()) and 
    loc = call.getLocation().getFile().getAbsolutePath() + ":" + call.getLocation().getStartLine()

select call.getCallee().toString() + "()","打印了可能存在敏感信息的变量: "+tempStr, " "+loc


