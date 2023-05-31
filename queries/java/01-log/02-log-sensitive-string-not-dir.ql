// import java

// from MethodAccess ma
// where ma.getMethod().hasName(["info", "error"]) and
//   ma.getQualifier().getType() instanceof RefType and
//   ma.getQualifier().(VarAccess).getVariable().getType().(RefType).hasQualifiedName("com.safeheron.gm.partner.api.api", "LogServiceApiV2") and
//   exists(string s |
//     s = ["requestBody", "APIkey"] and
//     ma.getAnArgument().(StringLiteral).getValue().matches("%" + s + "%")
//   )
// select ma, "This log statement may contain sensitive information."



// import java

// from MethodAccess ma
// where ma.getMethod().hasName(["info", "error"]) and
//   exists(string s |
//     s = ["requestBody", "Key"] and
//     ma.getAnArgument().(StringLiteral).getValue().matches("%" + s + "%")
//   )
// select ma, "This log statement may contain sensitive information."



// import java

// from MethodAccess ma, Variable v
// where ma.getMethod().hasName(["info","error"]) and
//   exists(Expr arg |
//     arg = ma.getAnArgument() and
//     arg.(VarAccess).getVariable() = v and
//     exists(string s |
//       s = ["userPublicKey"] and
//       v.getName().matches("%" + s + "%")
//     )
//   )
// select ma, "This log statement may contain sensitive information."

import java
import semmle.code.java.dataflow.TaintTracking

class LoggingCall extends MethodAccess {
  LoggingCall() {
    this.getMethod().hasName(["info", "error", "debug", "warn", "trace"]) and
    this.getMethod().getNumberOfParameters() >= 1 and
    this.getMethod().getParameterType(0) instanceof TypeString
  }
}

class SensitiveVar extends Variable {
  SensitiveVar() { this.getName().toLowerCase().regexpMatch(".*(?i)(key|password|secret|vault|arn|arn|email|content|mail|ldap|message|response|request).*") }//这里填写要匹配的字符串
}

class LogTaintConfig extends TaintTracking::Configuration {
  LogTaintConfig() { this = "LogTaintConfig" }

  override predicate isSource(DataFlow::Node source) {
    source.asExpr() = any(SensitiveVar sv).getAnAccess()
  }

  override predicate isSink(DataFlow::Node sink) {
    sink.asExpr() = any(LoggingCall lc).getAnArgument()
  }
}

from LoggingCall lc, SensitiveVar sv, DataFlow::Node source, DataFlow::Node sink
where lc.getAnArgument() = sink.asExpr()
and source.asExpr() = sv.getAnAccess()
and any(LogTaintConfig config).hasFlow(source, sink)
select lc, lc.getLocation(), "打印了可能存在敏感信息的变量: \"" + sv.getName()+"\""