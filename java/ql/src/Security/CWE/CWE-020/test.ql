import java
import semmle.code.java.dataflow.TaintTracking

class XSS extends TaintTracking::Configuration {
  XSS() { this = "XSS" }

  override predicate isSource(DataFlow::Node source) {
    source.asDataFlowNode().asExpr() instanceof StringLiteral
  }

  override predicate isSink(DataFlow::Node sink) {
    sink.asDataFlowNode().asExpr() instanceof MethodAccess and
    exists(MethodAccess ma |
      ma.getMethod().getName() = "write" and
      ma.getQualifier().getType().toString().matches(".*(Writer|PrintWriter)")
    )
  }
}

from XSS cfg, DataFlow::PathNode source, DataFlow::PathNode sink
where cfg.hasFlowPath(source, sink)
select sink.getNode(), source, sink, "Possible XSS: " + source.asDataFlowNode().asExpr().toString()
