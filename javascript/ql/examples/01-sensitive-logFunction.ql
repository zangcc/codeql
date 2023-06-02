import javascript
import DataFlow

from PropRead pr ,string tempStr
where pr.getBase().toString().regexpMatch("(?i)(log)") and
 // 循环判断每个参数是否包含敏感词
 exists(int i | i in [0 .. pr.getAMethodCall().getNumArgument() - 1] |
 pr.getAMethodCall().getArgument(i).asExpr().toString().regexpMatch("(?i).*(key|password|secret|vault|param|arn|text|email|content|token|mail|ldap|response|request).*") and 
 not pr.getAMethodCall().getArgument(i).asExpr() instanceof StringLiteral and 
 tempStr = pr.getAMethodCall().getArgument(i).toString())


select pr,"打印了可能存在敏感信息的变量: "+tempStr,pr.getFile().getAbsolutePath()+":"+pr.getStartLine()
