import java
import semmle.code.java.dataflow.DataFlow

class LoggingCall extends MethodAccess {
  LoggingCall() {
    this.getMethod().hasName(["info", "error", "debug", "warn", "trace"]) and
    this.getMethod().getNumberOfParameters() >= 1 and
    this.getMethod().getParameterType(0) instanceof TypeString
  }
}

class SensitiveVar extends Variable {
  SensitiveVar() {
    this.getName().toLowerCase().regexpMatch(".*(?i)(key|password|secret|vault|arn|arn|email|content|mail|ldap|message|response|request).*")
  }
}


from LoggingCall lc, SensitiveVar sv, DataFlow::Node arg1, DataFlow::Node arg2
where lc.getAnArgument() = arg2.asExpr() and 
      DataFlow::localFlow(DataFlow::exprNode(sv.getAnAccess()), arg1) and 
      DataFlow::localFlow(arg1, arg2)
select lc, lc.getLocation(), "打印了可能存在敏感信息的变量: \"" + sv.getName()+"\""

