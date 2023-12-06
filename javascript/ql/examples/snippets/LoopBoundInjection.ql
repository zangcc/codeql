/**
 * @name Loop bound injection
 * @description Iterating over an object with a user-controlled .length
 *              property can cause indefinite looping.
 * @kind path-problem
 * @problem.severity warning
 * @security-severity 7.5
 * @id js/loop-bound-injection
 * @tags security
 *       external/cwe/cwe-834
 *       external/cwe/cwe-730
 * @precision high
 */

import javascript
import semmle.javascript.security.dataflow.LoopBoundInjectionQuery
import DataFlow::PathGraph

from Configuration dataflow, DataFlow::PathNode source, DataFlow::PathNode sink
where dataflow.hasFlowPath(source, sink)
select sink.getNode().asExpr().getFile().getAbsolutePath()+"$$"+sink.getNode().asExpr().getFile().getLocation().getStartLine(),sink.getLocation().getFile().getAbsolutePath()+"$$"+sink.getLocation().getStartLine() ,sink, source, sink,
  "Iteration over a user-controlled object with a potentially unbounded .length property from a $@.",
  source, "user-provided value"
